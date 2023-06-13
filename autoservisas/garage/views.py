from typing import Any, Dict, Optional
from django.shortcuts import render,  get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from . models import Car, Order, Service
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import ListView
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, reverse
from django.utils.translation import gettext_lazy as _
from . forms import OrderReviewForm
from django.contrib import messages
from django.views import generic
from datetime import date, timedelta
from django.urls import reverse, reverse_lazy
from . forms import OrderRequestForm


def index(request):
    services_count = Service.objects.all().count()
    orders_completed = Order.objects.filter(status__exact="delivered").count()
    cars_count = Car.objects.all().count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'services_count': services_count,
        'orders_completed': orders_completed,
        'cars_count': cars_count,
        'num_visits': num_visits,
    }
    return render(request, 'garage/index.html', context)

def car_list(request):
    qs = Car.objects
    query = request.GET.get('query')
    if query:
        qs = qs.filter(
            Q(model__brand__istartswith=query)|
            Q(model__model__istartswith=query)
        )
    else:
        qs = qs.all()

    paginator = Paginator(qs, 3)
    car_list = paginator.get_page(request.GET.get('page'))
    return render(request, 'garage/car_list.html', {'car_list': car_list})


def service_list(request):
    paginator = Paginator(Service.objects.all(), 3)
    service_list = paginator.get_page(request.GET.get("page"))
    return render(request, 'garage/service_list.html', {'service_list': service_list})

def car_detail(request, pk: int):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'garage/car_detail.html', {'car': car})


class OrderListView(ListView):
    model = Order
    context_object_name = 'orders'
    paginate_by = 3
    template_name = 'garage/order_list.html'


class OrderDetailView(generic.edit.FormMixin, generic.DetailView):
    model = Order
    template_name = 'garage/order_detail.html'
    form_class = OrderReviewForm

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['total_price'] = sum(entry.price for entry in self.get_object().order_entries.all())
        return context

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        initial['order'] = self.get_object()
        initial['reviewer'] = self.request.user
        return initial

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form: Any) -> HttpResponse:
        form.instance.book = self.get_object()
        form.instance.reviewer = self.request.user
        form.save()
        messages.success(self.request, _('Review posted!'))
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('order_detail', kwargs={'pk':self.get_object().pk})
    

class UserCarListView(LoginRequiredMixin, ListView):
    model = Car
    template_name = 'garage/user_car_list.html'
    context_object_name = 'car_list'
    paginate_by = 3

    def get_queryset(self):
        return Car.objects.filter(customer=self.request.user)
    

class UserOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'garage/user_orders_list.html'
    paginate_by = 3

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(car__customer=self.request.user)
        return qs
    

class CarOrderRequestView(generic.CreateView):
    model = Order
    form_class = OrderRequestForm
    template_name = 'garage/order_request_form.html'
    success_url = reverse_lazy('order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['car'] = self.get_car()
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['car'] = self.get_car()
        initial['due_back'] = date.today() + timedelta(days=14)
        initial['status'] = 'new'
        return initial

    def form_valid(self, form):
        form.instance.car = self.get_car()
        form.instance.status = 'new'
        return super().form_valid(form)

    def get_car(self):
        car_id = self.kwargs.get('pk')
        car = Car.objects.get(id=car_id)
        return car
    

class OrderUpdateView(
        LoginRequiredMixin, 
        UserPassesTestMixin, 
        generic.UpdateView
    ):
    model = Order
    form_class = OrderRequestForm
    template_name = 'garage/order_request_form.html'
    success_url = reverse_lazy('order_list')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        if obj.status == 'new':
            context['updating'] = True
        else:
            context['extending'] = True
        return context

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        initial['due_back'] = date.today() + timedelta(days=14)
        initial['status'] = 'new'
        return initial

    def form_valid(self, form):
        form.instance.status = 'new'
        return super().form_valid(form)

    def test_func(self) -> bool | None:  
        obj = self.get_object()
        return obj.customer == self.request.user
    

class BookOrderDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.DeleteView
):
    model = Order
    template_name = 'garage/user_order_delete.html'
    success_url = reverse_lazy('order_list')

    def test_func(self) -> bool | None:
        obj = self.get_object()
        return obj.customer == self.request.user

        
from django.shortcuts import render,  get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from . models import Car, Order, Service
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import ListView
from django.db.models.query import QuerySet


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

def order_detail(request, pk: int):
    order = get_object_or_404(Order, pk=pk)
    total_price = sum(entry.price for entry in order.order_entries.all())

    return render(request, 'garage/order_detail.html', {'order': order, 'total_price': total_price})


class OrderListView(ListView):
    model = Order
    context_object_name = 'orders'
    paginate_by = 3
    template_name = 'garage/order_list.html'

class UserOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'garage/user_orders_list.html'
    paginate_by = 3

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(car__customer=self.request.user)
        return qs
    
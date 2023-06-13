from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name = "index"),
    
    path('cars/', views.car_list, name='car_list'),  
    path('services/', views.service_list, name='service_list'), 
    path('cars/<int:pk>/', views.car_detail, name='car_detail'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/my/', views.UserOrderListView.as_view(), name='user_orders_list'),
    path('cars/my/', views.UserCarListView.as_view(), name='user_car_list'),
    path('car/order_request/<int:pk>/', views.CarOrderRequestView.as_view(), name='order_request_form'),
    path('car/update/<int:pk>/', views.OrderUpdateView.as_view(), name='order_update'),
    path('car/return/<int:pk>/', views.BookOrderDeleteView.as_view(), name='order_delete'),
]

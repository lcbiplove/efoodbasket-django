from django.urls import path
from . import views

urlpatterns = [
    path('ajax/order/place/', views.PlaceOrderView.as_view(), name='place_order'),
    path('orders/<pk>/', views.OrderDetailView.as_view(), name='order_detail'),
]

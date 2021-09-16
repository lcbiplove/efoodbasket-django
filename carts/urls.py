from django.urls import path
from . import views

urlpatterns = [
    path('ajax/vouchers/check/', views.VoucherCheckView.as_view(), name='voucher_check'),
    path('carts/', views.CartListView.as_view(), name='cart_list'),
    path('ajax/carts/add/', views.CartCreateView.as_view(), name='cart_create'),
]

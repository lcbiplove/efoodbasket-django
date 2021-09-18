from django.urls import path
from . import views

urlpatterns = [
    path('ajax/vouchers/check/', views.VoucherCheckView.as_view(), name='voucher_check'),
    path('carts/', views.CartListView.as_view(), name='cart_list'),
    path('ajax/carts/add/', views.CartCreateView.as_view(), name='cart_create'),
    path('ajax/carts/<pk>/delete/', views.CartDeleteView.as_view(), name='cart_delete'),
    path('ajax/carts/delete-multiple/', views.CartDeleteMultipleView.as_view(), name='cart_delete_multiple'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('shops/', views.ShopListView.as_view(), name='shop_list'),
    path('shops/add/', views.ShopCreateView.as_view(), name='shop_create'),
    path('shops/<pk>/edit/', views.ShopUpdateView.as_view(), name='shop_update'),
    path('shops/<pk>/delete/', views.ShopDeleteView.as_view(), name='shop_delete'),
]

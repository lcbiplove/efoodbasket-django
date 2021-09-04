from django.urls import path
from . import views

urlpatterns = [
    path('shops/', views.ShopListView.as_view(), name='shop_list'),
    path('shops/add/', views.ShopCreateView.as_view(), name='shop_create'),
    path('shops/<pk>/edit/', views.ShopUpdateView.as_view(), name='shop_update'),
    path('shops/<pk>/delete/', views.ShopDeleteView.as_view(), name='shop_delete'),
    path('products/add/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/manage/', views.ManageProductView.as_view(), name='product_manage'),
    path('products/<pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/<pk>/edit/', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('traders/<pk>/products/visit/', views.VisitTraderView.as_view(), name='visit_trader'),
]

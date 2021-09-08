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
    path('traders/<pk>/products/visit/', views.VisitTraderView.as_view(), name='visit_trader'),
    path('ajax/products/<pk>/add-query/', views.QueryCreateView.as_view(), name='query_create'),
    path('ajax/products/<id>/delete-query/<pk>/', views.QueryDeleteView.as_view(), name='query_delete'),
    path('ajax/products/<id>/add-answer/<pk>/', views.AnswerUpdateView.as_view(), name='answer_create'),
    path('ajax/products/<id>/delete-answer/<pk>/', views.AnswerDeleteView.as_view(), name='answer_delete'),
    path('ajax/products/<pk>/add-rating/', views.RatingCreateUpdateView.as_view(), name='rating_create'),
    path('ajax/products/<pk>/add-review/', views.ReviewCreateUpdateView.as_view(), name='review_create'),
    path('ajax/products/<id>/delete-review/<pk>/', views.ReviewDeleteView.as_view(), name='review_delete'),
    path('wishlists/', views.WishListView.as_view(),name='wishlist_list'),
    path('ajax/products/<id>/wishlists/add/', views.WishCreateView.as_view(), name='wishlist_create'),
    path('ajax/products/<id>/wishlists/delete/', views.WishDeleteView.as_view(), name='wishlist_delete'),
]

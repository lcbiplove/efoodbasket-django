from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('notifications/', views.NotificationListView.as_view(), name='notification_list'),
    path('ajax/notifications/<pk>/make-seen/', views.NotificationUpdateView.as_view(), name='notification_update'),
]

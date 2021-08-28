from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('auth/<id>/verify-email/', views.VerifyEmailView.as_view(), name='verify_email'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signup-trader/', views.SignupTraderView.as_view(), name='signup_trader'),
    path('accounts/<id>/verify-email/', views.VerifyEmailView.as_view(), name='verify_email'),
    path('accounts/reset/<uidb64>/<token>/', views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('accounts/manage/', views.ManageAccountView.as_view(), name='manage_account'),
    path('accounts/change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('admin/trader-requests/<pk>/', views.TraderRequestsDetailView.as_view(), name='trader_request'),
]

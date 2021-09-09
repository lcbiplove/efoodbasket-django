from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse

class UserNotRequired(UserPassesTestMixin):
    
    def test_func(self) -> bool:
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('/')

class AdminPermission(LoginRequiredMixin, UserPassesTestMixin):
    
    def test_func(self):
        return self.request.user.is_staff

class TraderRequired(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_trader

class CustomerRequired(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_customer
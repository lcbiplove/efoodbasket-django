from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect

class UserNotRequired(UserPassesTestMixin):
    
    def test_func(self) -> bool:
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('/')

class AdminPermission(LoginRequiredMixin, UserPassesTestMixin):
    
    def test_func(self):
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        return redirect('/')

class TraderRequired(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_trader
    
    def handle_no_permission(self):
        return redirect('/')

class CustomerRequired(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_customer
    
    def handle_no_permission(self):
        return redirect('/')
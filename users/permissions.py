from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class UserNotRequired(UserPassesTestMixin):
    
    def test_func(self) -> bool:
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('/')

class AdminPermission(UserPassesTestMixin):
    
    def test_func(self):
        return self.request.user.is_staff

class TraderRequired(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_trader
    
    def handle_no_permission(self):
        return redirect('/')
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import request

class OrderOwnerRequired(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        self.object = self.get_object()
        return self.object.payment.user.id == self.request.user.id
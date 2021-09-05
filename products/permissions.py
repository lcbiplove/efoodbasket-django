from users.permissions import TraderRequired
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

class ShopOwnerRequired(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        self.object = self.get_object()
        has_perm = self.request.user.is_staff
        if self.request.user.is_trader:
            return self.request.user.trader == self.object.trader
        return has_perm


class ProductOwnerRequired(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        self.object = self.get_object()
        has_perm = self.request.user.is_staff 
        if self.request.user.is_trader:
            return self.request.user.trader == self.object.shop.trader 
        return has_perm

class QuestionOwnerRequired(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        self.object = self.get_object()
        return self.request.user.id == self.object.user.id

class AnswerOwnerRequired(TraderRequired):

    def test_func(self):
        super().test_func()
        self.object = self.get_object()
        return self.request.user.trader.id == self.object.product.shop.trader.id

class ReviewOwnerRequired(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        self.object = self.get_object()
        return self.request.user.id == self.object.rating.user.id
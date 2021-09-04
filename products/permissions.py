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
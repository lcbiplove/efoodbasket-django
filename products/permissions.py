from django.contrib.auth.mixins import UserPassesTestMixin

class ShopOwnerRequired(UserPassesTestMixin):

    def test_func(self):
        self.object = self.get_object()
        return self.request.user.trader == self.object.trader

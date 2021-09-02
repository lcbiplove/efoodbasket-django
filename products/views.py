from django.core.checks import messages
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from .models import Shop
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .permissions import ShopOwnerRequired
from users.permissions import TraderRequired
from django.contrib import messages


class ShopCreateView(SuccessMessageMixin, TraderRequired, CreateView):
    model = Shop
    template_name = 'add-shop.html'
    fields = ['name', 'address', 'contact']
    success_message = 'Shop Added successfully!'

    def dispatch(self, request, *args, **kwargs):
        shop_count = Shop.objects.filter(trader__id=self.request.user.trader.id).count()
        if shop_count >= 2:
            messages.add_message(request, messages.INFO, 'You can only add upto 2 shops.', 'info')
            return redirect('shop_list')
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.instance.trader = self.request.user.trader
        return form

class ShopUpdateView(SuccessMessageMixin, ShopOwnerRequired, UpdateView):
    model = Shop
    template_name = 'edit-shop.html'
    context_object_name = 'shop'
    fields = ['name', 'address', 'contact']
    success_message = 'Shop updated successfully!'

class ShopListView(ListView):
    model = Shop
    template_name = 'shops.html'
    context_object_name = 'shops'

    def get_queryset(self):
        return Shop.objects.filter(trader__user__id=self.request.user.id).select_related('trader', 'trader__user')

class ShopDeleteView(ShopOwnerRequired, DeleteView):
    model = Shop
    success_url = reverse_lazy('shop_list')

from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from .models import Shop
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .permissions import ShopOwnerRequired
from users.permissions import TraderRequired


class ShopCreateView(SuccessMessageMixin, TraderRequired, CreateView):
    model = Shop
    template_name = 'add-shop.html'
    fields = ['name', 'address', 'contact']
    success_message = "Shop Added successfully!"

    def form_valid(self, form):
        form.instance.trader = self.request.user.trader
        return super().form_valid(form)

class ShopUpdateView(SuccessMessageMixin, ShopOwnerRequired, UpdateView):
    model = Shop
    template_name = 'edit-shop.html'
    context_object_name = 'shop'
    fields = ['name', 'address', 'contact']
    success_message = "Shop updated successfully!"

class ShopListView(ListView):
    model = Shop
    template_name = 'shops.html'
    context_object_name = 'shops'

    def get_queryset(self):
        return Shop.objects.filter(trader__user__id=self.request.user.id)

class ShopDeleteView(ShopOwnerRequired, DeleteView):
    model = Shop
    success_url = reverse_lazy('shop_list')

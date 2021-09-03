from django.core.checks import messages
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from .models import ProductCategory, Shop, ProductImage
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .permissions import ShopOwnerRequired
from users.permissions import TraderRequired
from django.contrib import messages
from .forms import CreateProductForm

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

    def get_success_url(self):
        success_url = super().get_success_url()
        next_page = self.request.GET.get('next')
        if next_page:
            success_url = next_page
        return success_url

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


class ProductCreateView(SuccessMessageMixin, TraderRequired, CreateView):
    form_class = CreateProductForm
    template_name = 'add-product.html'
    success_message = 'Product Added successfully!'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if not Shop.objects.filter(trader__user__id=self.request.user.id).exists():
            messages.add_message(request, messages.INFO, 'You need to have at least a shop to add product.', 'info')
            return redirect(reverse_lazy('shop_create') + '?next=' + reverse_lazy('product_create'))
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shops'] = Shop.objects.filter(trader__user__id=self.request.user.id)
        context['categories'] = ProductCategory.objects.all()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.trader = self.request.user.trader
        self.object.save()
        img_files = form.files.getlist('image')
        for file in img_files:
            ProductImage.objects.create(image=file, product=self.object)
        return super().form_valid(form)

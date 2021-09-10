from django.db.models.aggregates import Count
from django.views.generic import ListView, CreateView
from django.http.response import JsonResponse
from django.db.models import F
from .models import Cart, CollectionSlot

class CartListView(ListView):
    model = Cart
    template_name = 'cart.html'
    context_object_name = 'carts'

    def get_queryset(self):
        return self.model.objects.filter(user__id=self.request.user.id).select_related('product', 'product__shop')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collection_slots'] = CollectionSlot.objects.all()
        # context['collection_days'] = CollectionSlot.objects.values('day') \
        #                                                     .annotate(day_count=Count('day'))
        return context
    
class CartCreateView(CreateView):
    model = Cart
    fields = ['quantity', 'product']

    def form_valid(self, form):
        quantity = form.cleaned_data.get("quantity")
        product = form.cleaned_data.get("product")
        self.object, _ = Cart.objects.get_or_create(
                product=product,
                user=self.request.user,
                defaults={
                    'quantity': quantity
                }
            )
        if not _:
            self.object.quantity = F('quantity') + quantity
            self.object.save()
        return JsonResponse({
            'total_items': Cart.get_carts_count(self.request.user),
            'message': 'Product added to cart.',
            'type': 'success',
        })

    def form_invalid(self, form):
        return JsonResponse({'error': str(form.errors)})
from django.views.generic import View, ListView, CreateView
from django.http.response import JsonResponse
from django.forms.models import model_to_dict
from django.db.models import F
from django.views.generic.base import View
from .models import Cart, CollectionSlot, Voucher


class VoucherCheckView(View):
    def post(self, request, *args, **kwargs):
        code = request.POST.get('code')
        response = {
            'message': 'Invalid voucher code.',
            'type': 'fail',
        }
        qs = Voucher.objects.filter(code=code)
        
        if qs.exists():
            response['message'] = 'Voucher code "{}" applied.'.format(code)
            response['type'] = 'success'            
            response['data'] = model_to_dict(qs.first())
        
        return JsonResponse(response)


class CartListView(ListView):
    model = Cart
    template_name = 'cart.html'
    context_object_name = 'carts'

    def get_queryset(self):
        return self.model.objects.filter(user__id=self.request.user.id).select_related('product', 'product__shop')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collection_slots'] = CollectionSlot.objects.all()
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
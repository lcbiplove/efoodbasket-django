from django.views.generic import View, DetailView, ListView
from django.http.response import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Payment, Order, OrderProduct
from carts.models import Cart
from efoodbasket import notifications
from django.db.models import F
from users.permissions import CustomerRequired
from .permissions import OrderOwnerRequired


class OrderListView(CustomerRequired, ListView):
    model = Order
    template_name = 'orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return self.model.objects.filter(payment__user__id=self.request.user.id)
    


class OrderDetailView(OrderOwnerRequired, DetailView):
    model = Order
    template_name = 'order.html'
    context_object_name = 'order'


class PlaceOrderView(LoginRequiredMixin, View):
    
    def post(self, request, *args, **kwargs):
        payment_data = {
            'amount': request.POST.get('amount'),
            'paypal_payer_id': request.POST.get('paypal_payer_id'),
            'paypal_order_id': request.POST.get('paypal_order_id'),
            'user': request.user
        }
        payment = Payment.objects.create(**payment_data)
        voucher_id= request.POST.get('voucher_id')
        order_data = {
            'collection_date': request.POST.get('collection_date'),
            'collection_slot_id': request.POST.get('collection_slot_id'),
            'payment': payment
        }
        if voucher_id != 'null' and voucher_id:
            order_data['voucher_id'] = voucher_id

        order = Order.objects.create(**order_data)

        cart_products = Cart.objects.filter(user_id=request.user.id).only('product', 'quantity')
        
        order_products_list = []
        order_product_response = []
        for cart_obj in cart_products:
            my_dict = {}
            my_dict['order_id'] = order.id
            my_dict['product_id'] = cart_obj.product.id
            my_dict['quantity'] = cart_obj.quantity
            item_obj = OrderProduct(**my_dict)
            notifications.notif_order_placed_trader(item_obj)
            order_products_list.append(item_obj)

            cart_obj.product.quantity =  F('quantity') - cart_obj.quantity
            cart_obj.product.save()

            my_response_obj = {
                'quantity': my_dict['quantity'],
                'discount': cart_obj.product.discount,
                'price': cart_obj.product.price,
                'image': str(cart_obj.product.thumbnail_url()),
                'product_name': cart_obj.product.name,
            }
            order_product_response.append(my_response_obj)

        OrderProduct.objects.bulk_create(order_products_list)

        notifications.notif_order_placed_customer(
            user=request.user,
            order=order,
            collection_date=order_data['collection_date'],
            cartItemsCount=Cart.get_carts_count(request.user)
        )

        cart_products.delete()
        return JsonResponse({
            'order_id': order.id,
            'orderProduct': order_product_response,
            'collectionDate': order_data['collection_date'],
        })

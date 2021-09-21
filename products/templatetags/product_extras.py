from django import template
from products.models import Product, WishList

register = template.Library()


@register.simple_tag(takes_context=True)
def is_in_wish_list(context, product_id) -> bool:
    request = context.get("request")
    user = request.user
    return WishList.objects.filter(user__id=user.id, product__id=product_id).exists()

@register.simple_tag(takes_context=True)
def user_has_ordered_product(context, product) -> bool:
    request = context.get("request")
    user = request.user
    if not user.is_authenticated:
        return 
        
    return Product.user_has_ordered_product(user=user, product=product)


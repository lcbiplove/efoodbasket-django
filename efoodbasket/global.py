from home.models import Notification
from products.models import ProductCategory

def categories(request):
    return  {
        'categories': ProductCategory.objects.all()
    }

def notification_count(request):
    notif_dict = {'notification_count': 0}
    if request.user.is_authenticated:
        notif_dict['notification_count'] = Notification.user_unseen_count(user=request.user)
    return notif_dict
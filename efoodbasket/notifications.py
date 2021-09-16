from home.models import Notification
from django.templatetags.static import static
from django.urls import reverse

def notify_welcome_user(user):
    Notification.objects.create(
        title='Welcome to efoodbasket',
        body='Hi, we are happy to see you in our platform. We hope you have a great experience with us. We will be looking for your feedback.',
        image_link=static('images/efoodbasket-logo.png'),
        sender_text='From efoodbasket',
        main_link='#',
        user=user
    )

def notify_welcome_trader(user):
    Notification.objects.create(
        title='Welcome to efoodbasket',
        body='Hi, we are happy to see you here. We hope to collaborate with you forever. We will be looking for your feedback and support.',
        image_link=static('images/efoodbasket-logo.png'),
        sender_text='From efoodbasket',
        main_link='#',
        user=user
    )

def notify_dashboard_pw(user):
    import secrets
    random_pass = secrets.token_urlsafe(10)
    Notification.objects.create(
        title='Dashboard Login',
        body=f"You can login to your dashboard to analyse and manage products. Your dashboard login username and password are: <p>Username: <b><i>{user.email}</i></b></p><p>Password: <b><i>{random_pass}</i></b></p>",
        image_link=static('images/notif-dashboard.png'),
        sender_text='From efoodbasket',
        main_link='#',
        user=user
    )

def notify_question(query):
    user = query.product.shop.trader.user
    Notification.objects.create(
        title='Query about product',
        body=f"You have recieved a query on your product: \"{query.question[:50]}\"",
        image_link=static('images/notif-question.png'),
        sender_text='From efoodbasket',
        main_link=reverse('product_detail', kwargs={'pk': query.product.id}) + f"?is_notif=true&query_id={query.id}",
        user=user
    )

def notif_answer(query):
    user = query.user
    Notification.objects.create(
        title='Answer about product',
        body=f"Your query about a product is answerd: \"{query.answer[:50]}\"",
        image_link=static('images/notif-answer.png'),
        sender_text='From efoodbasket',
        main_link=reverse('product_detail', kwargs={'pk': query.product.id}) + f"?is_notif=true&query_id={query.id}",
        user=user
    )

def notif_order_placed_customer(cartItemsCount, order, user, collection_date):
    Notification.objects.create(
        title='Order Placed',
        body=f"Your order of {cartItemsCount} "+ (cartItemsCount > 1 and "items" or "item") + f" is placed. You will be able to collect them from collection slot after {collection_date}.",
        image_link=static('images/notif-order.png'),
        sender_text='From efoodbasket',
        main_link=reverse('order_detail', kwargs={'pk': order.id}),
        user=user
    )

def notif_order_placed_trader(orderProduct):
    Notification.objects.create(
        title='Order Received',
        body="Customer has ordered {orderProduct.quantity} "+ (orderProduct.quantity > 1 and "items" or "item") +" of "+orderProduct.product.name+" from your shop.",
        image_link=static('images/notif-order.png'),
        sender_text='From efoodbasket',
        main_link=reverse('product_detail', kwargs={'pk': orderProduct.product.id}),
        user=orderProduct.product.shop.trader.user
    )

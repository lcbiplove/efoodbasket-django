from django.db import models
from users.models import User


class Notification(models.Model):
    title = models.CharField(max_length=255)
    body = models.CharField(max_length=1000)
    sender_text = models.CharField(max_length=255)
    main_link = models.CharField(max_length=255, default='#')
    image_link = models.CharField(max_length=1000)
    notified_date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
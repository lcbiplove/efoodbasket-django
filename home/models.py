from django.db import models
from users.models import User
from django.db.models import Count


class Notification(models.Model):
    title = models.CharField(max_length=255)
    body = models.CharField(max_length=1000)
    sender_text = models.CharField(max_length=255)
    main_link = models.CharField(max_length=255, default='#')
    image_link = models.CharField(max_length=1000)
    notified_date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')

    def __str__(self):
        return self.title

    def is_not_link(self):
        return self.main_link != '#'

    @staticmethod
    def user_unseen_count(user):
        return Notification.objects.filter(user__id=user.id, is_seen=False).aggregate(
                unseen_count=Count('id')
            )['unseen_count']
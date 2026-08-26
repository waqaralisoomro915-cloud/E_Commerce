from django.db import models
from .. accounts.models import User
class Notification(models.Model):
    class NotificationType(models.TextChoices):
        ORDER='ORDER','order'
        PAYMENT='PAYMENT','payment'
        SHIPPING='SHIPPING','shipping'
        DELIVERY='DELIVERY','delivery'
        COUPONS='COUPONS','coupons'
        SYSTEM='SYSTEM','system'

    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='notifications')
    notificationType=models.CharField(choices=NotificationType.choices,default=NotificationType.ORDER,max_length=10)
    title = models.CharField(max_length=100)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
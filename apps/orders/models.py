from django.db import models
from ..accounts.models import User
from ..addresses.models import Address
class Order(models.Model):
    class Status(models.TextChoices):
        PENDING ='PENDING','pending'
        CONFIRMED ='CONFIRMED','confirmed'
        SHIPPED ='SHIPPED','shipped'
        DELIVERED = 'DELIVERED','delivered'
        CANCELLED = 'CANCELLED','cancelled'
    user = models.ForeignKey(User,on_delete=models.PROTECT,related_name='orders')
    address=models.ForeignKey(Address,on_delete=models.PROTECT,related_name='orders')
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    status= models.CharField(max_length=20,choices=Status.choices, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
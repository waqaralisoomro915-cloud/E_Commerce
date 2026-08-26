from django.db import models
from ..accounts.models import User
from ..addresses.models import Address
from ..coupons.models import Coupons
class Order(models.Model):
    class Status(models.TextChoices):
        PENDING ='PENDING','pending'
        CONFIRMED ='CONFIRMED','confirmed'
        SHIPPED ='SHIPPED','shipped'
        DELIVERED = 'DELIVERED','delivered'
        CANCELLED = 'CANCELLED','cancelled'
    user = models.ForeignKey(User,on_delete=models.PROTECT,related_name='orders')
    address=models.ForeignKey(Address,on_delete=models.PROTECT,related_name='orders')
    coupon = models.ForeignKey(Coupons,on_delete=models.PROTECT,related_name='orders',blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    subtotal = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    discount_amount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    status= models.CharField(max_length=20,choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
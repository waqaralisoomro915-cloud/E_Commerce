from django.db import models
from ..cart.models import Cart
from ..products.models import Product

class CartItems(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.PROTECT,related_name='cart_items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return f'{self.product.name} {self.quantity}'


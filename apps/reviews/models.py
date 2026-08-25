from django.db import models
from ..accounts.models import User
from ..products.models import Product
from ..orders.models import Order
from django.core.validators import MinValueValidator, MaxValueValidator
class Review(models.Model):
    user = models.ForeignKey(User,on_delete=models.PROTECT,related_name='reviews')
    product = models.ForeignKey(Product,on_delete=models.PROTECT,related_name='reviews')
    order = models.ForeignKey(Order,on_delete=models.PROTECT,related_name='reviews')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    comment = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user','product','order'],
                name='unique_rating'

            )
        ]
    def __str__(self):
        return f' {self.product.name} {self.rating}'
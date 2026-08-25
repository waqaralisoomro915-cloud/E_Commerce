from django.db import models
from ..accounts.models import User
from ..products.models import Product


class WishList(models.Model):
    user =models.OneToOneField(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.user.user}'s wishlist"

class WishListItem(models.Model):
    wishlist = models.ForeignKey(WishList,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['wishlist','product'],
                name='unique_product_wishlist'
            )
        ]
    def __str__(self):
        return self.product.name

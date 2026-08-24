from django.db import models
from ..accounts.models import User

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
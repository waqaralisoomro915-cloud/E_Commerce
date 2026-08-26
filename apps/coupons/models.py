from django.db import models

class Coupons(models.Model):
    class DiscountType(models.TextChoices):
        PERCENTAGE = 'PERCENTAGE','percentage'
        FIXED = 'FIXED','fixed'
    code=models.CharField(max_length=10, unique=True)
    discount_type = models.CharField(max_length=10, choices=DiscountType.choices)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    maximum_order_amount = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField()
    usage_limit=models.PositiveIntegerField(null=True, blank=True)
    used_count = models.PositiveIntegerField(null=True, blank=True,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.code


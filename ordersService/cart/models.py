
from django.db import models

from products.models import Product

class Cart(models.Model):
    user_id = models.IntegerField() 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Quantity user wants
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User {self.user_id} - {self.product.name} ({self.quantity})"

from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('available', 'Available'), ('out_of_stock', 'Out of Stock')])
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

from rest_framework import serializers
from .models import Cart
from products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "description", "status", "quantity"]

class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True
    ) 
    class Meta:
        model = Cart
        fields = ["id", "user_id", "product", "product_id" ,"quantity", "added_at"]

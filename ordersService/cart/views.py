from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Cart
from .serializers import CartSerializer

# 📌 1. Add Product to Cart
@api_view(['POST'])
def add_to_cart(request):
    data = request.data.copy()
    serializer = CartSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(product_id=data["product"])
        return Response({"message": "Product added to cart!", "cart": serializer.data}, status=201)
    return Response(serializer.errors, status=400)

# 📌 2. Get Cart Items by User
@api_view(['GET'])
def get_cart(request, user_id):
    cart_items = Cart.objects.filter(user_id=user_id)
    serializer = CartSerializer(cart_items, many=True)
    return Response(serializer.data)

# 📌 3. Update Cart Item (Only Quantity)
@api_view(['PUT'])
def update_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    new_quantity = request.data.get("quantity")

    if new_quantity and int(new_quantity) > 0:
        cart_item.quantity = int(new_quantity)
        cart_item.save()
        return Response({"message": "Cart updated successfully!", "cart": CartSerializer(cart_item).data}, status=200)
    
    return Response({"error": "Invalid quantity"}, status=400)

# 📌 4. Delete Cart Item
@api_view(['DELETE'])
def delete_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    cart_item.delete()
    return Response({"message": "Cart item deleted!"}, status=204)

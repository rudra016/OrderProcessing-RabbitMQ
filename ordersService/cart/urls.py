from django.urls import path
from .views import add_to_cart, get_cart, update_cart, delete_cart

urlpatterns = [
    path('add/', add_to_cart, name='add_to_cart'),   # Add product to cart
    path('user/<int:user_id>/', get_cart, name='get_cart'),  # Get all cart items for a user
    path('update/<int:cart_id>/', update_cart, name='update_cart'),  # Update cart item
    path('delete/<int:cart_id>/', delete_cart, name='delete_cart'),  # Delete cart item
]

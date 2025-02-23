from django.urls import path
from .views import create_order, list_orders, update_order, delete_order

urlpatterns = [
    path('create/', create_order, name='create_order'),
    path('list/', list_orders, name='list_orders'),
    path('update/<int:order_id>/', update_order, name='update_order'),  
    path('delete/<int:order_id>/', delete_order, name='delete_order'),  
]

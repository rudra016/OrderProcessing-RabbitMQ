from django.urls import path
from .views import list_products, get_product

urlpatterns = [
    path('', list_products, name='list_products'),
    path('<int:product_id>/', get_product, name='get_product'),
]

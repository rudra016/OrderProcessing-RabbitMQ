from django.shortcuts import get_object_or_404
from dotenv import load_dotenv
import os
# Create your views here.
import pika
import json
from django.conf import settings
import ssl
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from decimal import Decimal

load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL")

def decimal_to_float(obj):

    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Type {type(obj)} not serializable")

def publish_to_user_service(user_id, event_type, order_data):
  
    params = pika.URLParameters(RABBITMQ_URL)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
  
    params.ssl_options = pika.SSLOptions(context)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue="user_validation_queue")


    message = json.dumps({ 
        "user_id": user_id,
        "event": event_type,
        "order": order_data,
    },
    default=decimal_to_float 
    )

   

    channel.basic_publish(exchange='', routing_key="user_validation_queue", body=message.encode("utf-8"))

    connection.close()

@api_view(['POST'])
def create_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        user_id = serializer.validated_data['user_id']
        
        # Send message to User Management service
        publish_to_user_service(user_id, "Order created", serializer.validated_data)


        serializer.save()
        return Response({"message": "Order created, waiting for user validation!", "order": serializer.data}, status=201)

    return Response(serializer.errors, status=400)

@api_view(['GET'])
def list_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
def update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    serializer = OrderSerializer(order, data=request.data, partial=True)  # `partial=True` allows updating only some fields
    if serializer.is_valid():
        serializer.save()

        publish_to_user_service(order.user_id, "Order updated", serializer.validated_data)

        return Response({"message": "Order updated successfully!", "order": serializer.data}, status=200)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return Response({"message": "Order deleted successfully!"}, status=204)
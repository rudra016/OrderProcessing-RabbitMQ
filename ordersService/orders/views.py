from django.shortcuts import render

# Create your views here.
import pika
import json
from django.conf import settings
import ssl
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer

RABBITMQ_URL = "amqps://mrxifpeh:5ngDkk7VFF_rhmziwX0uW8jOzcyzQRLJ@collie.lmq.cloudamqp.com/mrxifpeh"

def publish_to_user_service(user_id):
  
    params = pika.URLParameters(RABBITMQ_URL)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
  
    params.ssl_options = pika.SSLOptions(context)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue="user_validation_queue")

    message = json.dumps({"user_id": user_id})
    channel.basic_publish(exchange='', routing_key="user_validation_queue", body=message)

    connection.close()

@api_view(['POST'])
def create_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        user_id = serializer.validated_data['user_id']
        
        # Send message to User Management service
        publish_to_user_service(user_id)

        serializer.save()
        return Response({"message": "Order created, waiting for user validation!", "order": serializer.data}, status=201)

    return Response(serializer.errors, status=400)

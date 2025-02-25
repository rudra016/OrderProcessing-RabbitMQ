# Orders Service - E-commerce Platform

## Overview
The Orders Service is a Django-based microservice for handling order processing, cart management, and product retrieval in a simulated e-commerce platform. It communicates with the User Management Service via RabbitMQ for user-related operations.

## Features

- Order Management (Create, List, Update, Delete Orders)

- Cart Management (Add, Retrieve, Update, Delete Cart Items)

- Product Retrieval (List and Get Product Details)

- RabbitMQ integration for message-based communication

- PostgreSQL as the primary database

- Sentry for error tracking

- OpenAPI (Swagger) documentation for API reference

## Directory Structure
```
ordersService/
│-- orders/        # Order-related functionality
│-- cart/          # Cart-related functionality
│-- products/      # Product retrieval functionality
│-- manage.py      # Django project management script
│-- .env   
```
### API Endpoints
Orders (```/orders``` prefix)

- POST ```/create/```
Create a new order

- GET ```/list/```
List all orders

- PUT ```/update/<order_id>/```
Update an order

- DELETE
```/delete/<order_id>/```
Delete an order

Cart (```/cart``` prefix)

- POST ```/add/```
Add a product to the cart

- GET ```/user/<user_id>/```
Get all cart items for a user

- PUT ```/update/<cart_id>/```
Update a cart item

- DELETE
```/delete/<cart_id>/```
Delete a cart item

## Installation and Setup

### Prerequisites

 - Python 3.8+

 - PostgreSQL

 - RabbitMQ

 - Virtual Environment (venv)

## Environment Variables

Create a .env file in the root directory and set the following variables
```
RABBITMQ_URL=your_rabbitmq_url
POSTGRES_PASSWD=your_postgres_password
SENTRY_DSN=your_sentry_dsn
```

## First-time Setup
Cloning and Setting Up
```
git clone https://github.com/rudra016/OrderProcessing-RabbitMQ.git

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

```
cd ordersService
pip install -r requirements.txt
create .env
```
Running the Server
```
python manage.py makemigrations
python manage.py migrate

python manage.py runserver 8001
```

## API Documentation

Swagger/OpenAPI documentation is available at:
127.0.0.1:8001/docs#/

## Load Testing
For load testing details, refer to [Load Testing](https://locustreport.tiiny.site).

## Deployment Instructions

#### Docker-based Deployment

- Install Docker and Docker Compose.

- Create a docker-compose.yml file in the root directory with the necessary configurations for Django, PostgreSQL, and RabbitMQ.

- Build and start the containers:
```
docker-compose up --build -d
```

- Run database migrations inside the running Django container:
```
docker exec -it orders_service_container python manage.py migrate
```

- The service should now be running and accessible at http://127.0.0.1:8001.

from locust import HttpUser, task, between
import random
import time

class OrderUser(HttpUser):
    wait_time = between(1, 3)
    order_ids = []  # Store created order IDs

    def on_start(self):
        """Ensure there is at least one order at the beginning"""
        payload = {
            "user_id": random.randint(1, 1000),
            "product_name": f"Product-{random.randint(1, 100)}",
            "quantity": random.randint(1, 10),
            "price": round(random.uniform(10, 500), 2),
            "description": "Initial test order",
            "status": "pending"
        }
        response = self.client.post("/orders/create/", json=payload)
        if response.status_code == 201:
            order_id = response.json().get("id")
            if order_id:
                self.order_ids.append(order_id)
                print(f"Initial Order {order_id} created successfully")

    @task(2)
    def list_orders(self):
        """Fetch all orders and store IDs"""
        response = self.client.get("/orders/list/")
        if response.status_code == 200:
            orders = response.json()
            if orders and isinstance(orders, list):
                self.order_ids = [order["id"] for order in orders]  # Store valid order IDs
                print("Order list updated with existing orders")

    @task(3)
    def create_order(self):
        """Create a new order and store its ID"""
        payload = {
            "user_id": random.randint(1, 1000),
            "product_name": f"Product-{random.randint(1, 100)}",
            "quantity": random.randint(1, 10),
            "price": round(random.uniform(10, 500), 2),
            "description": "Test order",
            "status": "pending"
        }
        response = self.client.post("/orders/create/", json=payload)
        if response.status_code == 201:
            order_id = response.json().get("id")
            if order_id:
                self.order_ids.append(order_id)
                print(f"Order {order_id} created successfully")

    @task(2)
    def update_order(self):
        """Update an existing order if available"""
        if not self.order_ids:
            self.list_orders()  # Fetch orders if list is empty
            time.sleep(1)  # Allow time for orders to be fetched

        if self.order_ids:
            order_id = random.choice(self.order_ids)
            payload = {"status": "shipped"}
            response = self.client.put(f"/orders/update/{order_id}/", json=payload)
            if response.status_code == 200:
                print(f"Order {order_id} updated successfully")

    @task(1)
    def delete_order(self):
        """Delete an existing order if available"""
        if not self.order_ids:
            self.list_orders()
            time.sleep(1)

        if self.order_ids:
            order_id = self.order_ids.pop()
            response = self.client.delete(f"/orders/delete/{order_id}/")
            if response.status_code == 200:
                print(f"Order {order_id} deleted successfully")

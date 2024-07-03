import logging
from ..utils.gps import coords_by_address, dist_between_coords
import requests
import time
import json

class Drone:
    def __init__(self):
        self.remaining_range = 25.00
        self.pizza_store = (34.22142886882653, -119.18323113902395)
        self.current_coords = self.pizza_store
        self.next_coords = None

        try:
            response = requests.get("http://localhost:5000/order/find-path")
            response.raise_for_status()
            self.data = response.json()
            self.path = self.data['path']
            self.dist = self.data['distance']
            self.addresses = self.data['addresses']
            logging.warning(f"Addresses: {self.addresses}\nPath: {self.path}\nDistance: {self.dist}\n")
        except requests.RequestException as e:
            logging.error(f"Error fetching path data: {e}")
            self.data = {}
            self.path = []
            self.dist = 0
            self.addresses = []

    def get_next_order(self):
        if not self.path:
            logging.warning("No orders to process.")
            return

        for idx in self.path:
            address = self.addresses[idx]
            logging.info(f"Getting next order at address: {address}")

            self.next_coords = coords_by_address(address)
            self.deliver_pizza(idx, self.next_coords)

        logging.info("No orders left. Returning to store...")
        self.current_coords = self.pizza_store

    def deliver_pizza(self, order_id, next_coords):
        logging.info(f"Current coordinates: {self.current_coords}")

        miles_to_address = dist_between_coords(self.current_coords, next_coords)
        miles_to_store = dist_between_coords(next_coords, self.pizza_store)
        est_range = round(miles_to_address + miles_to_store, 2)

        logging.info(f"Range remaining: {self.remaining_range} miles")
        logging.info(f"Estimated range: {est_range} miles")

        if self.remaining_range >= est_range:
            logging.info(f"Delivering order {order_id} to address: {next_coords}")
            self.current_coords = next_coords
            self.remaining_range = round(self.remaining_range - miles_to_address, 2)
            time.sleep(2)
            try:
                response = requests.post(f"http://localhost:5000/orders/deliver-order/{order_id}")
                response.raise_for_status()
                status = response.json().get('status', 'success')
                logging.info(f"Order {order_id} delivery status: {status}")
            except requests.RequestException as e:
                logging.error(f"Error delivering order: {e}")
        else:
            logging.info("Returning to pizza store for new battery...")
            self.return_to_store()

    def return_to_store(self):
        self.current_coords = self.pizza_store
        self.remaining_range = 25.00
        logging.info("Drone returned to store and recharged.")

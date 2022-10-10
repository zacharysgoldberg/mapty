from .gps import coords_by_address, dist_between_coords
import requests
from models import User, Order
import time
import json

# [Drone object]


class Drone:
    # [Drone attributes]
    def __init__(self):
        self.remaining_range = 25.00
        self.pizza_store = (34.22142886882653, -119.18323113902395)
        self.current_coords = ()
        self.access_token = True
        self.data = json.loads(requests.get(
            "http://localhost:8000/orders/optimize-path").text)
        # [Optimal path id order]
        # self.orders = [order for order in self.data['orders']]
        # print(self.orders)
        # self.addresses = [
        #     Order.get(pk).address for pk in self.data['orders']]
        # print(self.addresses)

    # [Making request to database for auth and order]
    def get_next_order(self):
        for order in self.orders:
            # [Ensure drone is authenticated before requesting next order]
            # if self.access_token is None:
            #     print("\nAuthenticating Drone...\n")
            #     token = requests.post("http://localhost:8000/auth/token",
            #                                                             data={"username": "ExampleUser", "password": "test1234!"})
            #     self.access_token = token.cookies

            if self.access_token:
                print('----- Drone Authenticated -----\nGetting next order...\n')
                response = requests.get(
                    f"http://localhost:8000/orders/get-next-order/{order}", cookies=self.access_token)

                if response.text != 'false':
                    address = json.loads(response.text)['address']

                    print('Next order address:', address)

                    self.next_coords = coords_by_address(address)
                    self.deliver_pizza(self.next_coords)

            else:
                print('*** Drone Credentials Are Invalid ***\n')
                return

        print('No orders left. Returning to store...')
        print('Current coordinates: -----', self.current_coords, '-----')
        self.current_coords = self.pizza_store

    # [Delivery logic]

    def deliver_pizza(self, next_coords):
        if len(self.current_coords) == 0:
            self.current_coords = self.pizza_store

        if self.current_coords == self.pizza_store:
            print('Leaving from: Pizza Store')

        print('Current coordinates: -----', self.current_coords, '-----')
        # [Calculating estimated range for drone to travel to address and back to store]
        miles_to_address = dist_between_coords(
            self.current_coords, next_coords)
        self.miles_to_store = dist_between_coords(
            next_coords, self.pizza_store)
        est_range = round(miles_to_address + self.miles_to_store, 2)

        print("Range remaining:", self.remaining_range, "miles")
        print("\nEstimated range:", est_range, "miles")

        # [In the event the est range to deliver and return to base is less than remaining range, return to store for new battery]
        if self.remaining_range >= est_range:
            print('\nDelivering pizza...')
            # [Set new current coordinates and new remaining range]
            self.current_coords = next_coords
            self.remaining_range = round(self.remaining_range -
                                         miles_to_address - self.miles_to_store, 2)
            time.sleep(2)
            # [Ppdating database for delivery to True]
            response = requests.post(
                f"http://localhost:8000/orders/deliver-order/{order}", cookies=self.access_token)

            if response.text == 'true':
                print('Pizza delivered successfully\nWaiting for next order...\n')
                time.sleep(2)

            return False

        else:
            print('\nReturning to pizza store for new battery...\n')
            time.sleep(2)
            self.return_to_store()

    # [Resetting current coordinates and remaining range for drone upon returning to base]
    def return_to_store(self):
        self.current_coords = self.pizza_store
        self.remaining_range = 25.00

        print('Attempting to re-deliver order...\n')
        # [Attempting redelivery of order]
        self.deliver_pizza(self.next_coords)
        time.sleep(2)

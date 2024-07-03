import csv
import os
from app.data.models import Order


# Function to read CSV and insert into database
def read_csv_and_insert(file_path) -> list:
    orders: list = []
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found.")
    
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            order = Order(
                address=row['address'],
                delivered=row['delivered'].strip().lower() == 'true'
            )
            orders.append(order)
    return orders
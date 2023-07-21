import os
import requests

def get_all_orders():
    try:
        response = requests.get(os.environ.get('ORDERS_API_URL'))
        response.raise_for_status()
        orders_data = response.json()
        return orders_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching orders from the API: {e}")
        return []
    
def get_all_items():
    try:
        response = requests.get(os.environ.get('INVENTORY_API_URL'))
        response.raise_for_status()
        items_data = response.json()
        return items_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching items from the API: {e}")
        return []
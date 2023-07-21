import os

def env():
    os.environ["ORDERS_API_PORT"] = "8010"
    os.environ["INVENTORY_API_PORT"] = "8011"
    os.environ["PAYMENT_API_PORT"] = "8012"
    os.environ["SHIPPING_API_PORT"] = "8013"

    os.environ["ORDERS_API_URL"] = f"http://127.0.0.1:{os.environ.get('ORDERS_API_PORT')}/orders/"
    os.environ["INVENTORY_API_URL"] = f"http://127.0.0.1:{os.environ.get('INVENTORY_API_PORT')}/items/"
    os.environ["PAYMENT_API_URL"] = f"http://127.0.0.1:{os.environ.get('PAYMENT_API_PORT')}/payments/"
    os.environ["SHIPPING_API_URL"] = f"http://127.0.0.1:{os.environ.get('SHIPPING_API_PORT')}/shipping/"
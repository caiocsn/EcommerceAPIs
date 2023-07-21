import os
import threading
import time
import uvicorn
import init
import contextlib

from GUI.Main import MainApplication
from InventoryAPI.main import app as inventory_app
from OrdersAPI.main import app as orders_app
from PaymentAPI.main import app as payment_app
from ShippingAPI.main import app as shipping_app

class Server(uvicorn.Server):
    def install_signal_handlers(self):
        pass

    @contextlib.contextmanager
    def run_in_thread(self):
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()

init.env()

inventory_api_port = int(os.environ.get('INVENTORY_API_PORT'))
orders_api_port = int(os.environ.get('ORDERS_API_PORT'))
payment_api_port = int(os.environ.get('PAYMENT_API_PORT'))
shipping_api_port = int(os.environ.get('SHIPPING_API_PORT'))

config = uvicorn.Config(orders_app, host="127.0.0.1", port=orders_api_port)
order_server = Server(config=config)

config = uvicorn.Config(inventory_app, host="127.0.0.1", port=inventory_api_port)
inventory_server = Server(config=config)

config = uvicorn.Config(payment_app, host="127.0.0.1", port=payment_api_port)
payment_server = Server(config=config)

config = uvicorn.Config(shipping_app, host="127.0.0.1", port=shipping_api_port)
shipping_server = Server(config=config)

def run_servers():
    config = uvicorn.Config(orders_app, host="127.0.0.1", port=5000)
    server = Server(config=config)
    server.run_in_thread()

with order_server.run_in_thread():
    with inventory_server.run_in_thread():
        with payment_server.run_in_thread():
            with shipping_server.run_in_thread():
                    app = MainApplication()
                    app.mainloop()
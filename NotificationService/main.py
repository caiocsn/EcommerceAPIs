import os 
import sys
import time

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from sqlalchemy import event
from models.db_models import OrderDB, Base

'''def notify_user(order_id, new_status):
    print(f"Order {order_id} status changed to: {new_status}")

def handle_status_change(mapper, connection, target):
    original_order = connection.get_transaction().original_order

    if original_order.status != target.status:
        notify_user(target.id, target.status)

event.listen(OrderDB, 'before_update', handle_status_change)   ''' 

@event.listens_for(OrderDB.metadata, 'before_create')
def receive_after_create(target, connection, **kw):    
    print("Base class before commit!")

if __name__ == "__main__":    
    print("Microservice started. Watching for changes...")
    
    try:
        while True:
            pass

    except KeyboardInterrupt:
        print("Microservice stopped.")
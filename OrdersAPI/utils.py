import os 
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

import requests
from typing import Dict

import init

init.env()

def call_subtract_items_api(items: Dict[int, int]) -> int:
    url = f"http://127.0.0.1:{os.environ.get('INVENTORY_API_PORT')}/items/subtract/"

    response = requests.put(url, json=items)

    return response


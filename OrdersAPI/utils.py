import requests
from typing import Dict

def call_subtract_items_api(items: Dict[int, int]) -> int:
    url = "http://127.0.0.1:8000/items/subtract/"

    response = requests.put(url, json=items)

    return response.status_code


from src.shopping_list.catalog import catalog
import re
import requests
import json
import logging
import os

logger = logging.getLogger(__name__)

cart_url = "https://www.rami-levy.co.il/api/v2/cart"
token_url = "https://api-prod.rami-levy.co.il/api/v2/site/auth/login"

json_headers = {
    'Content-Type': 'application/json'
}

RAMY_USER = os.environ.get('RAMY_USER')
RAMY_PASS = os.environ.get('RAMY_PASS')
STORE = os.environ.get('STORE')
ECOMTOKEN = os.environ.get('ECOMTOKEN')

token_payload = json.dumps({
    "username": RAMY_USER,
    "password": RAMY_PASS,
    "id_delivery_times": None
})

headers = {
    'ecomtoken': "",
    'Content-Type': 'application/json'
}

payload = {
    "store": STORE,
    "isClub": 0,
    "supplyAt": "2022-07-17T00:00:00.000Z",
    "items": {},
    "meta": None
}

local_cart_items = []


def get_items(bot_data, cart_item):
    if len(bot_data) == 0:
        bot_data["items"], bot_data["items_reverse"] = catalog.get_all_items()
    items = bot_data["items"]
    item_reg = re.compile(cart_item)
    cart_items = []
    for item in items.items():
        if item_reg.search(item[0]):
            cart_items.append(item)
    return cart_items


def get_local_items():
    return local_cart_items


def clear_local_items():
    local_cart_items.clear()


def add_local_item(item):
    global local_cart_items
    local_cart_items.append(item)


def add_items_cart(items):
    logger.info("adding items to online cart")
    cart_items = {}
    for item in local_cart_items:
        cart_items[item] = "1.00"
    # headers['ecomtoken'] = get_token()
    headers[
        'ecomtoken'] = ECOMTOKEN
    payload["items"] = cart_items
    response = requests.request("POST", cart_url, headers=headers, data=json.dumps(payload))
    logger.info("response from ramy\n %s", response.json())


def get_token():
    logger.info("getting token")
    response = requests.request("POST", token_url, headers=json_headers, data=token_payload)
    return response.json()['user']['token']

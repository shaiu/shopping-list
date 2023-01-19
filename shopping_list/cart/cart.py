"""Rami Levy cart methods"""
import json
import logging
import os

import requests

logger = logging.getLogger(__name__)

CART_URL = "https://www.rami-levy.co.il/api/v2/cart"
TOKEN_URL = "https://api-prod.rami-levy.co.il/api/v2/site/auth/login"

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

LOCAL_CART_ITEMS = []


def get_cart_items():
    """
    get local cache of items
    :return: local_cart_items
    """
    return LOCAL_CART_ITEMS


def clear_cart_items():
    """
    clear local cache
    """
    LOCAL_CART_ITEMS.clear()


def add_cart_item(item):
    """
    add item to local cache
    :param item: item to add
    """
    LOCAL_CART_ITEMS.append(item)


def upload_items_cart():
    """
    upload items to Rami Levi cart
    """
    logger.info("adding items to online cart")
    cart_items = {}
    for item in LOCAL_CART_ITEMS:
        cart_items[item] = "1.00"
    headers['ecomtoken'] = ECOMTOKEN
    payload["items"] = cart_items
    response = requests.request(
        "POST", CART_URL, headers=headers, data=json.dumps(payload), timeout=10)
    logger.info("response from ramy\n %s", response.json())

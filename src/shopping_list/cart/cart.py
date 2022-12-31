"""Rami Levy cart methods"""
import json
import logging
import os
import re

import requests

from shopping_list.catalog import catalog

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


def get_items(bot_data, cart_item):
    """
    get all items that match the cart item
    this method compiles the cart_item to a regex and then looks for matches from the catalog
    :param bot_data: bot context that holds the items from the catalog
    :param cart_item: the item we are looking for
    :return:
    """
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
    """
    get local cache of items
    :return: local_cart_items
    """
    return LOCAL_CART_ITEMS


def clear_local_items():
    """
    clear local cache
    """
    LOCAL_CART_ITEMS.clear()


def add_local_item(item):
    """
    add item to local cache
    :param item: item to add
    """
    LOCAL_CART_ITEMS.append(item)


def add_items_cart():
    """
    add items to Rami Levi cart
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

"""Rami Levy catalog methods"""
import json
import logging
import os
import pathlib
import re

import requests

logger = logging.getLogger(__name__)

CATALOG_URL = "https://www.rami-levy.co.il/api/catalog?"

STORE = os.environ.get('STORE')

payload = {
    "store": STORE,
}

payload_from = {
    "store": STORE,
    "from": 0
}


class Catalog:

    def __init__(self, path, catalog_url) -> None:
        self.path = path if (path is not None) else pathlib.Path(__file__).parent.resolve()
        self.catalog_url = catalog_url if (catalog_url is not None) else CATALOG_URL
        self._all_items = []

    def search_for_item(self, cart_item):
        """
        get all items that match the cart item
        this method compiles the cart_item to a regex and then looks for matches from the catalog
        :param cart_item: the item we are looking for
        :return:
        """
        item_reg = re.compile(cart_item)
        return list(filter(lambda item: item_reg.search(item["name"]), self._all_items))

    def load_all_items(self):
        """
        Gets all items from all departments (from file departments.json)
        from the CATALOG_URL
        :return: all_name_to_id - dictionary name to id
                 all_id_to_name - dictionary id to name
        """

        logger.info("getting all items from site")
        with open(os.path.join(self.path, 'departments.json'), encoding="utf-8") as file:
            departments = json.load(file)
        for department in departments:
            payload["d"] = department
            payload_from["d"] = department
            response = requests.request("POST", self.catalog_url, data=payload, timeout=10)
            total = response.json()['total']
            for i in range(0, total, 30):
                payload_from["from"] = i
                response = requests.request("POST", self.catalog_url, data=payload_from, timeout=10)
                data = response.json()['data']
                self._all_items.extend(list(map(lambda x: {'name': x['name'], 'id': x['id']}, data)))

"""Rami Levy catalog methods"""
import json
import logging
import os
import pathlib
import re
import time

import requests

logger = logging.getLogger(__name__)

CATALOG_URL = "https://www.rami-levy.co.il/api/catalog?"

STORE = os.environ.get('STORE')

PAYLOAD = {
    "store": STORE,
}

PAYLOAD_FROM = {
    "store": STORE,
    "from": 0
}


def load_department(department, catalog_url):
    department_items = []
    payload = PAYLOAD.copy()
    payload_from= PAYLOAD_FROM.copy()
    payload["d"] = department
    payload_from["d"] = department
    logger.info(f"department {department}")
    response = requests.request("POST", catalog_url, data=payload, timeout=10)
    try:
        total = response.json()['total']
    except requests.exceptions.JSONDecodeError:
        logger.error("no total")
        return []
    logger.info(f"total is {total} department {department}")
    for i in range(0, total, 30):
        logger.info(f"going over items from {i} department {department}")
        payload_from["from"] = i
        response = requests.request("POST", catalog_url, data=payload_from, timeout=10)
        try:
            data = response.json()['data']
            department_items.extend(
                list(map(
                    lambda x:
                    {
                        'name': x['name'],
                        'id': x['id'],
                        'price': x['price']['price'],
                    }, data)))
        except requests.exceptions.JSONDecodeError:
            logger.error(f"not json - department <{department}>, payload_from {payload_from}, status_code {response.status_code}, headers {response.headers}")
            payload_from_from = payload_from['from']
            with open(os.path.join(f'error_response_{department}_{payload_from_from}.html'), mode='w') as f:
                f.write(response.text)
    return department_items


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
        filtered_list = list(filter(lambda item: item_reg.search(item["name"]), self._all_items))
        return sorted(filtered_list, key=lambda x: x['price'])

    def load_all_items(self, sleep_time=20):
        """
        Gets all items from all departments (from file departments.json)
        from the CATALOG_URL
        :return: all_name_to_id - dictionary name to id
                 all_id_to_name - dictionary id to name
        """

        logger.info("getting all items from site")
        with open(os.path.join(self.path, 'departments.json'), encoding="utf-8") as file:
            departments = json.load(file)
        logger.info(f"departments are {departments}")

        for department in departments:
            self._all_items.extend(load_department(department, self.catalog_url))
            time.sleep(sleep_time)

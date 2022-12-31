"""Rami Levy catalog methods"""
import json
import logging
import os
import pathlib

import requests

logger = logging.getLogger(__name__)

c_path = pathlib.Path(__file__).parent.resolve()

CATALOG_URL = "https://www.rami-levy.co.il/api/catalog?"

STORE = os.environ.get('STORE')

payload = {
    "store": STORE,
}

payload_from = {
    "store": STORE,
    "from": 0
}


def get_all_items():
    """
    Gets all items from all departments (from file departments.json)
    from the CATALOG_URL
    :return: all_name_to_id - dictionary name to id
             all_id_to_name - dictionary id to name
    """

    logger.info("getting all items from site")
    all_name_to_id = {}
    all_id_to_name = {}
    with open(os.path.join(c_path, 'departments.json'), encoding="utf-8") as file:
        departments = json.load(file)
    for department in departments:
        payload["d"] = department
        payload_from["d"] = department
        response = requests.request("POST", CATALOG_URL, data=payload, timeout=10)
        total = response.json()['total']
        for i in range(0, total, 30):
            payload_from["from"] = i
            response = requests.request("POST", CATALOG_URL, data=payload_from, timeout=10)
            data = response.json()['data']
            name_to_id = {data[i]["name"]: str(data[i]["id"]) for i in range(len(data))}
            id_to_name = {str(data[i]["id"]): str(data[i]["name"]) for i in range(len(data))}
            all_name_to_id.update(name_to_id)
            all_id_to_name.update(id_to_name)
    return all_name_to_id, all_id_to_name

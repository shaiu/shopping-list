import json
import logging
import os

import requests
import pathlib

logger = logging.getLogger(__name__)

c_path = pathlib.Path(__file__).parent.resolve()

url = "https://www.rami-levy.co.il/api/catalog?"

STORE = os.environ.get('STORE')

payload = {
    "d": 49,
    "store": STORE,
}

payload_from = {
    "d": 49,
    "store": STORE,
    "from": 0
}


def get_all_items():
    logger.info("getting all items from site")
    all_name_to_id = {}
    all_id_to_name = {}
    with open(os.path.join(c_path, 'departments.json')) as f:
        departments = json.load(f)
    for department in departments:
        payload["d"] = department
        payload_from["d"] = department
        response = requests.request("POST", url, data=payload)
        total = response.json()['total']
        for i in range(0, total, 30):
            payload_from["from"] = i
            response = requests.request("POST", url, data=payload_from)
            data = response.json()['data']
            name_to_id = {data[i]["name"]: str(data[i]["id"]) for i in range(len(data))}
            id_to_name = {str(data[i]["id"]): str(data[i]["name"]) for i in range(len(data))}
            all_name_to_id.update(name_to_id)
            all_id_to_name.update(id_to_name)
    # with open(os.path.join(c_path, 'items.json'), 'w') as f:
    #     json.dump(all_name_to_id, f, indent=6)
    return all_name_to_id, all_id_to_name

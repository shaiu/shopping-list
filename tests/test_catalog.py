import pathlib

import responses

from shopping_list.catalog import catalog


@responses.activate
def test_load_all_items():
    cat = catalog.Catalog(pathlib.Path(__file__).parent.resolve(), "https://test/api/catalog")

    responses._add_from_file(file_path="out.toml")

    cat.load_all_items()
    assert len(cat._all_items) == 267

    items = cat.search_for_item('תפוח')
    assert len(items) == 14

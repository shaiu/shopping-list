import os
import pathlib
import responses

from shopping_list.catalog import catalog


@responses.activate
def test_load_all_items():
    cat = catalog.Catalog(pathlib.Path(__file__).parent.resolve(), "https://test/api/catalog")

    responses._add_from_file(file_path=os.path.join(pathlib.Path(__file__).parent.resolve(), "out.yaml"))

    cat.load_all_items(0)
    assert has_duplicates(cat._all_items) is False
    assert len(cat._all_items) == 485

    items = cat.search_for_item('תפוח')
    assert len(items) == 14
    assert items[0]['id'] == 13
    assert items[0]['name'] == 'תפוח אדמה לבן ארוז'
    assert items[0]['price'] == 3.9
    assert items[0]['department'] == 'פירות וירקות'


def has_duplicates(lst):
    seen = set()
    for d in lst:
        # Convert the dictionary to a tuple of its items
        t = tuple(d.items())
        # If we've seen this tuple before, it's a duplicate
        if t in seen:
            return True
        seen.add(t)
    return False
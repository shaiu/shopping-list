from src.shopping_list.cart import cart


def test_add_item_to_cart():
    bot_data = {'items': {'תפוח אדום': '1'}}
    items = cart.get_items(bot_data, "תפוח")
    assert len(items) == 1
    assert items[0][0] == 'תפוח אדום'
    assert items[0][1] == '1'

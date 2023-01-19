import logging
import os

from shopping_list.cart.cart import add_cart_item, get_cart_items
from shopping_list.catalog.catalog import Catalog

logging.basicConfig(level=logging.INFO)

from flask import Flask
from flask_restful import Resource, Api, reqparse

parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('name')

cat = Catalog(None, None)
cat.load_all_items()


class CatalogResource(Resource):
    def get(self, cart_item):
        return cat.search_for_item(cart_item)


class CartResource(Resource):
    def post(self):
        args = parser.parse_args()
        cart_item = {'id': args['id'], 'name': args['name']}
        return add_cart_item(cart_item)

    def get(self):
        return get_cart_items()


def create_app(test_config=None):
    # create and configure the app

    app = Flask(__name__, instance_relative_config=True)
    api = Api(app)

    api.add_resource(CatalogResource, '/catalog/<string:cart_item>')
    api.add_resource(CartResource, '/cart')

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000)

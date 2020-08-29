from flask import Blueprint
from flask_restful import Api

from .resources import UsersResources, CategorysResources, ProductsResources, OrdersResources

api_app = Blueprint('api', __name__)

api = Api(api_app)

api.add_resource(UsersResources,         '/users',    '/users/<id_user>')
api.add_resource(CategorysResources,     '/categorys', '/categorys/<id_category>')
api.add_resource(ProductsResources,      '/products', '/products/<id_product>')
api.add_resource(OrdersResources,        '/orders',   '/orders/<id_order>')
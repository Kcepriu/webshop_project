from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from ..db import Category, Product, User, New, Text, Order
from .schemas import UsersSchema, CategorysSchema, ProductsSchema, OrdersSchema

class UsersResources(Resource):
    def get(self, id_user=None):
        if id_user:
            obj = User.objects.get(id=id_user)
            return UsersSchema().dump(obj)

        objs = User.objects()
        return UsersSchema().dump(objs, many=True)

    def post(self):
        pass

    def put(self, id_user):
        pass

    def delete(self, id_user):
        product = User.objects().get(id=id_user)
        product.delete()
        return {'status': 'deleted'}

class CategorysResources(Resource):
    def get(self, id_category=None):
        if id_category:
            obj = Category.objects.get(id=id_category)
            return CategorysSchema().dump(obj)

        objs = Category.objects()
        return CategorysSchema().dump(objs, many=True)

    def post(self):
        pass

    def put(self, id_category):
        pass

    def delete(self, id_category):
        product = Category.objects().get(id=id_category)
        product.delete()
        return {'status': 'deleted'}

class ProductsResources(Resource):
    def get(self, id_product=None):
        if id_product:
            obj = Product.objects.get(id=id_product)
            return ProductsSchema().dump(obj)

        objs = Product.objects()
        return ProductsSchema().dump(objs, many=True)

    def post(self):
        pass

    def put(self, id_product):
        pass

    def delete(self, id_product):
        product = Product.objects().get(id=id_product)
        product.delete()
        return {'status': 'deleted'}

class OrdersResources(Resource):
    def get(self, id_order=None):
        if id_order:
            obj = Order.objects.get(id=id_order)
            return OrdersSchema().dump(obj)

        objs = Order.objects()
        return OrdersSchema().dump(objs, many=True)

    def post(self):
        pass

    def put(self, id_order):
        pass

    def delete(self, id_order):
        product = Order.objects().get(id=id_order)
        product.delete()
        return {'status': 'deleted'}
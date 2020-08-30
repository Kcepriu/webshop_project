from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from mongoengine.errors import OperationError, NotUniqueError

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
        try:
            res = UsersSchema().load(request.get_json())
            obj = User.objects.create(**res)
            return UsersSchema().dump(obj)
        except ValidationError as err:
            return {'error': err.messages}
        except NotUniqueError:
            return {'Error': 'Not Unique'}

    def put(self, id_user):
        try:
            res = UsersSchema().load(request.get_json())
            obj = User.objects().get(id=id_user)
            obj.update(**res)
            return UsersSchema().dump(obj.reload())
        except ValidationError as err:
            return {'error': err.messages}
        except NotUniqueError:
            return {'Error': 'Not Unique'}

    def delete(self, id_user):
        obj = User.objects().get(id=id_user)
        try:
            obj.delete()
            return {'status': 'deleted'}
        except OperationError as err:
            return {'error': err.messages}

        return {'status': 'deleted'}


class CategorysResources(Resource):
    def get(self, id_category=None):
        if id_category:
            obj = Category.objects.get(id=id_category)
            return CategorysSchema().dump(obj)

        objs = Category.objects()
        return CategorysSchema().dump(objs, many=True)

    def post(self):
        try:
            res = CategorysSchema().load(request.get_json())

            parent_id = res.get('parent', None)
            res['parent'] = None

            subcategories = res.get('subcategories', None)
            sub_category_obj = []
            for id_sub_category in subcategories:
                sub_category_obj.append(Category.objects.get(id=id_sub_category))
            res['subcategories'] = []

            obj = Category.objects().create(**res)
            obj.reload()

            if parent_id:
                Category.objects.get(id=parent_id).add_subcategory(obj)
            for sub_category in sub_category_obj:
                obj.add_subcategory(sub_category)

            return CategorysSchema().dump(obj.reload())
        except ValidationError as err:
            return {'error': err.messages}

    def put(self, id_category):
        try:
            res = CategorysSchema().load(request.get_json())
            parent_id = res.get('parent', None)

            res['parent'] = None

            subcategories = res.get('subcategories', None)

            sub_category_obj = []
            for id_sub_category in subcategories:
                sub_category_obj.append(Category.objects.get(id=id_sub_category))

            res['subcategories'] = []
            obj = Category.objects().get(id=id_category)
            if obj.parent:
                # Якщо вже є підкатегорією іншого обʼєкта, то треба видалити із списку суькатегорій батька
                obj.parent.subcategories.remove(obj)
                obj.parent.save()


            obj.update(**res)
            obj.reload()

            if parent_id:
                Category.objects.get(id=parent_id).add_subcategory(obj)
            for sub_category in sub_category_obj:
                obj.add_subcategory(sub_category)

            return CategorysSchema().dump(obj.reload())
        except ValidationError as err:
            return {'error': err.messages}

    def delete(self, id_category):
        obj = Category.objects().get(id=id_category)
        try:
            obj.delete()
            return {'status': 'deleted'}
        except OperationError as err:
            return {'error': err.messages}

        return {'status': 'deleted'}


class ProductsResources(Resource):
    def get(self, id_product=None):
        if id_product:
            obj = Product.objects.get(id=id_product)
            return ProductsSchema().dump(obj)

        objs = Product.objects()
        return ProductsSchema().dump(objs, many=True)

    def post(self):
        try:
            res = ProductsSchema().load(request.get_json())
            category_id = res.get('category', None)
            if category_id:
                res['category'] = Category.objects.get(id=category_id)
            obj = Product.objects.create(**res)
            return ProductsSchema().dump(obj)
        except ValidationError as err:
            return {'error': err.messages}
        except NotUniqueError:
            return {'Error': 'Not Unique'}

    def put(self, id_product):
        try:
            res = ProductsSchema().load(request.get_json())
            category_id = res.get('category', None)
            if category_id:
                res['category'] = Category.objects.get(id=category_id)
            obj = Product.objects().get(id=id_product)
            obj.update(**res)
            return ProductsSchema().dump(obj.reload())
        except ValidationError as err:
            return {'error': err.messages}

    def delete(self, id_product):
        obj = Product.objects().get(id=id_product)
        try:
            obj.delete()
            return {'status': 'deleted'}
        except OperationError as err:
            return {'error': err.messages}

        return {'status': 'deleted'}


class OrdersResources(Resource):
    def get(self, id_order=None):
        if id_order:
            obj = Order.objects.get(id=id_order)
            return OrdersSchema().dump(obj)

        objs = Order.objects()
        return OrdersSchema().dump(objs, many=True)

    def post(self):
        try:
            res = OrdersSchema().load(request.get_json())
            user_id = res.get('user', None)
            if user_id:
                res['user'] = User.objects.get(id=user_id)
            res['nom'] = Order.get_max_num_orders(res['user']) + 1

            obj = Order(**res)
            obj.sum = obj.get_sum_order()
            obj.save()
            return OrdersSchema().dump(obj.reload())
        except ValidationError as err:
            return {'error': err.messages}

    def put(self, id_order):
        try:
            res = OrdersSchema().load(request.get_json())
            user_id = res.get('user', None)
            if user_id:
                res['user'] = User.objects.get(id=user_id)

            obj = Order.objects().get(id=id_order)
            obj.update(**res)
            obj.reload()
            obj.sum = obj.get_sum_order()
            obj.save()
            return OrdersSchema().dump(obj.reload())
        except ValidationError as err:
            return {'error': err.messages}


    def delete(self, id_order):
        obj = Order.objects().get(id=id_order)
        try:
            obj.delete()
            return {'status': 'deleted'}
        except OperationError as err:
            return {'error': err.messages}

        return {'status': 'deleted'}
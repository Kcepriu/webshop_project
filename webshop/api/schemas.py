from marshmallow import Schema, fields, validate
from ..db import Order

class  UsersSchema(Schema):
    id = fields.String(validate=validate.Length(min=24, max=24), dump_only=True)
    user_id = fields.Integer(required=True)
    name = fields.String(validate=validate.Length(min=2, max=255))
    telephone = fields.String(validate=validate.Length(min=10, max=12))

class CategorysSchema(Schema):
    id = fields.String(validate=validate.Length(min=24, max=24), dump_only=True)
    title = fields.String(validate=validate.Length(min=2, max=512), required=True)
    description = fields.String(validate=validate.Length(min=8, max=2048))
    parent = fields.String(validate=validate.Length(min=0, max=24), allow_none=True)
    subcategories = fields.List(fields.String(validate=validate.Length(min=24, max=24), required=True))

class ParametersSchema(Schema):
    height = fields.Float()
    widht = fields.Float()
    length = fields.Float()
    weight = fields.Float()

class ProductsSchema(Schema):
    id = fields.String(validate=validate.Length(min=24, max=24), dump_only=True)
    title = fields.String(validate=validate.Length(min=2, max=512), required=True)
    description = fields.String(validate=validate.Length(min=8, max=2048))
    in_stock = fields.Integer(required=True)
    is_available = fields.Boolean(required=True)
    price = fields.Decimal(as_string=True)
    discount = fields.Integer()
    category = fields.String(validate=validate.Length(min=24, max=24), required=True)
    url_photo = fields.String(validate=validate.Length(min=4, max=255))
    parameters =  fields.Nested(ParametersSchema)

class Line_OrderSchema(Schema):
    product =fields.String(validate=validate.Length(min=24, max=24), required=True)
    count = fields.Integer(required=True)
    sum = fields.Decimal(as_string=True)


class OrdersSchema(Schema):
    id = fields.String(validate=validate.Length(min=24, max=24), dump_only=True)
    nom = fields.Integer(dump_only=True)
    date = fields.DateTime()
    user = fields.String(validate=validate.Length(min=24, max=24), required=True)
    sum = fields.Decimal(as_string=True, dump_only=True)
    telephone_recipients = fields.String(validate=validate.Length(min=10, max=12))
    name_recipients = fields.String(validate=validate.Length(min=3, max=255))

    products = fields.List(fields.Nested(Line_OrderSchema))

    status = fields.String(validate=validate.OneOf([elem[0] for elem in Order.STATUS_CONSTANT]), required=True)





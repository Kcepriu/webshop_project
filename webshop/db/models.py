import mongoengine as me
from decimal import  Decimal
from datetime import datetime

me.connect('webshopdb')

class Category(me.Document):
    title = me.StringField(min_length=2, max_length=512, required=True)
    description = me.StringField(min_length=8, max_length=2048)
    subcategories = me.ListField(me.ReferenceField('self'))
    parent = me.ReferenceField('self')

    def get_products(self):
        return Product.objects.filter(category=self)

    @classmethod
    def get_root_categories(cls):
        return cls.objects(parent=None)

    def add_subcategory(self, subcategory: 'Category'):
        subcategory.parent = self
        subcategory.save()

        self.subcategories.append(subcategory)
        self.save()

class Parameter(me.EmbeddedDocument):
    height = me.FloatField()
    widht = me.FloatField()
    length = me.FloatField()
    weight = me.FloatField()

class Product(me.Document):
    title = me.StringField(min_length=2, max_length=512, required=True)
    description= me.StringField(min_length=8, max_length=2048)
    parameters = me.EmbeddedDocumentField(Parameter)
    in_stock = me.IntField(min_value=0, required=True)
    is_available = me.BooleanField(default=True)
    price = me.DecimalField(min_value=1, force_string=True)
    discount = me.IntField(min_value=0, max_value=99,  default=0)
    category = me.ReferenceField(Category)

    @property
    def actual_price(self):
        return (self.price * Decimal((100 - self.discount) / 100)).quantize(Decimal('.01'), 'ROUND_HALF_UP')

    @classmethod
    def get_products_with_discount(cls):
        return cls.objects(discount__ne=0)


class New(me.Document):
    title = me.StringField(min_length=2, max_length=512, required=True)
    text = me.StringField(min_length=2, max_length=10240, required=True)
    date = me.DateTimeField(default=datetime.now())

    @classmethod
    def get_latest_news(cls, count_item=3):
        count_item = cls.objects.count()
        start_nom = count_item-count_item if count_item > count_item else 0
        return cls.objects[start_nom:]

class Text(me.Document):
    GRITINGS = 'greetings'
    DISCOUNT = 'discount'
    TITLES_CONSTANT = (
        (GRITINGS, 'greetings'),
        (DISCOUNT, 'discount')
    )
    title = me.StringField(required=True, choices=TITLES_CONSTANT, unique=True)
    body = me.StringField(min_length=4, max_length=4096)

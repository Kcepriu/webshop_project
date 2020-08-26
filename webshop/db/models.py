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
    url_photo = me.StringField(min_length=4, max_length=255)

    @property
    def actual_price(self):
        return (self.price * Decimal((100 - self.discount) / 100)).quantize(Decimal('.01'), 'ROUND_HALF_UP')

    @classmethod
    def get_products_with_discount(cls):
        return cls.objects(discount__ne=0)

class Line_Order(me.EmbeddedDocument):
    product = me.ReferenceField(Product)
    count = me.IntField(min_value=1)
    summ = me.DecimalField(min_value=1, force_string=True)

class Order(me.EmbeddedDocument):
    ORDER_CANCELED='canceled'
    ORDER_COMPLETED='completed'
    ORDER_ACTIVE='active'
    STATUS_CONSTANT = (
        (ORDER_CANCELED, 'order canceled'),
        (ORDER_COMPLETED, 'order completed'),
        (ORDER_ACTIVE, 'order active')
    )
    status = me.StringField(min_length=5, choices=STATUS_CONSTANT, default=ORDER_ACTIVE, required=True)
    date = me.DateTimeField(default=datetime.now())
    nom = me.IntField(min_value=1)
    products = me.EmbeddedDocumentListField(Line_Order)

class User(me.Document):
    user_id = me.IntField(unique=True, required=True)
    first_name = me.StringField(min_length=2, max_length=255)
    last_name = me.StringField(min_length=2, max_length=255)
    telephone = me.StringField(min_length=10, max_length=12, regex='^[0-9]*$')
    orders = me.EmbeddedDocumentListField(Order)

    @staticmethod
    def get_user(chat):
        user = User.objects(user_id=chat.id)
        if not user:
            user = User.objects.create(user_id=chat.id, first_name=chat.first_name if chat.first_name else '' ,
                                       last_name=chat.last_name if chat.last_name else '')
        else:
            user = user[0]
        return user

    def get_active_order(self):
        try:
            order = self.orders.get(status=Order.ORDER_ACTIVE)
        except me.DoesNotExist:
            order = None
        return order

    def create_order(self):
        return self.orders.create(nom=self.get_count_orders()+1)

    def add_product_to_order(self, product, count):
        active_orders = self.get_active_order()
        if not active_orders:
            active_orders = self.create_order()

        try:
            line_product = active_orders.products.get(product=product)
            line_product.count += count
            line_product.summ = line_product.count*product.actual_price
        except me.DoesNotExist:
            active_orders.products.create(product=product, count=count, summ=count*product.actual_price)
        self.save()

    def get_count_products_active_order(self):
        sums = User.objects(id=self.id).aggregate([
                {'$unwind': '$orders'},
                {'$match': {'orders.status': Order.ORDER_ACTIVE}},
                {'$unwind': '$orders.products'},
                {'$group': {'_id': '$_id', 'count_products': {'$sum': '$orders.products.count'}}}
            ])

        if sums.alive:
            elem = sums.next()
            return elem['count_products']
        else:
            return 0

    def get_count_orders(self):
        count_orders = User.objects(id=self.id).aggregate([
            {'$unwind': '$orders'},
            {'$match': {'orders.status': {'$ne': Order.ORDER_ACTIVE}}},
            {'$group': {'_id': '$_id', 'count_orders': {'$sum': 1}}}
        ])

        if count_orders.alive:
            elem = count_orders.next()
            return elem['count_orders']
        else:
            return 0

    def get_order_by_number(self, number):
        return self.orders[int(number)-1]

class Text(me.Document):
    GRITINGS = 'greetings'
    DISCOUNT = 'discount'
    ADD_TO_CART = 'add_to_cart'
    LIST_CATEGORYS = 'list_categorys'
    PRICE = 'price'
    RETURN_TO_TOP = 'return_to_the_top_level'
    PRODUCT_ADD_TO_CART = 'product_add_to_cart'

    START_KB_LIST_CATEGORYS = 'start_kb_list_categorys'
    START_KB_DISCOUNT = 'start_kb_discount'
    START_KB_NEWS = 'start_kb_news'
    GO_TO_CART = 'go_to_cart'
    ORDER_HISTORY = 'order_history'

    TITLES_CONSTANT = (
        (GRITINGS, 'greetings'),
        (DISCOUNT, 'discount'),
        (ADD_TO_CART, 'add to cart'),
        (PRICE, 'price'),
        (PRODUCT_ADD_TO_CART,  'product_add_to_cart'),
        (LIST_CATEGORYS, 'list_categorys'),
        (RETURN_TO_TOP, 'Return to the top level'),
        (START_KB_LIST_CATEGORYS, 'start_kb list categorys'),
        (START_KB_DISCOUNT, 'start_kb discount'),
        (START_KB_NEWS, 'start_kb news'),
        (GO_TO_CART, 'go_to_cart'),
        (ORDER_HISTORY, 'order_history')


    )
    title = me.StringField(required=True, choices=TITLES_CONSTANT, unique=True)
    body = me.StringField(min_length=4, max_length=4096)

    @staticmethod
    def get_body(title_):
        return Text.objects.get(title=title_).body

class New(me.Document):
    title = me.StringField(min_length=2, max_length=512, required=True)
    text = me.StringField(min_length=2, max_length=10240, required=True)
    date = me.DateTimeField(default=datetime.now())

    @classmethod
    def get_latest_news(cls, count_item=3):
        count_item = cls.objects.count()
        start_nom = count_item-count_item if count_item > count_item else 0
        return cls.objects[start_nom:]
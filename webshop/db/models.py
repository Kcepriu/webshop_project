import mongoengine as me
from mongoengine.queryset.visitor import Q
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


class User(me.Document):
    user_id = me.IntField(unique=True, required=True)
    first_name = me.StringField(min_length=2, max_length=255)
    last_name = me.StringField(min_length=2, max_length=255)
    telephone = me.StringField(min_length=10, max_length=12, regex='^[0-9]*$')

    @classmethod
    def get_user(cls, chat):
        user = cls.objects(user_id=chat.id)
        if not user:
            user = cls.objects.create(user_id=chat.id, first_name=chat.first_name if chat.first_name else '' ,
                                       last_name=chat.last_name if chat.last_name else '')
        else:
            user = user[0]
        return user


class Line_Order(me.EmbeddedDocument):
    product = me.ReferenceField(Product)
    count = me.IntField(min_value=1)
    summ = me.DecimalField(min_value=1, force_string=True)


class Order(me.Document):
    ORDER_ACTIVE = 'active'
    ORDER_PROCESSED = 'processed'
    ORDER_COMPLETED = 'completed'
    ORDER_CANCELED = 'canceled'

    STATUS_CONSTANT = (
        (ORDER_CANCELED, 'order canceled'),
        (ORDER_COMPLETED, 'order completed'),
        (ORDER_ACTIVE, 'order active'),
        (ORDER_PROCESSED, 'order processed')
    )
    nom = me.IntField(min_value=1)
    date = me.DateTimeField(default=datetime.now())
    user = me.ReferenceField(User)
    status = me.StringField(min_length=5, choices=STATUS_CONSTANT, default=ORDER_ACTIVE, required=True)
    products = me.EmbeddedDocumentListField(Line_Order)

    def get_text_status_order(self):
        if self.status == Order.ORDER_CANCELED:
            return 'Заказ отменен'
        elif self.status == Order.ORDER_ACTIVE:
            return 'Заказ редактируется'
        elif self.status == Order.ORDER_COMPLETED:
            return 'Заказ выполнен'
        else:
            return 'Заказ орабатывается'


    @classmethod
    def find_active_order(cls, user: User):
        try:
            order = cls.objects().get(Q(user=user) and Q(status=Order.ORDER_ACTIVE))
        except me.DoesNotExist:
            order = None
        return order

    @classmethod
    def get_count_orders(cls, user: User):
        return cls.objects(user=user).count()

    @classmethod
    def create_order(cls, user: User):
        return cls.objects.create(user=user, nom=cls.get_count_orders(user)+1)

    @classmethod
    def get_active_order(cls, user: User):
        active_orders = cls.find_active_order(user)
        if not active_orders:
            active_orders = cls.create_order(user)
        return active_orders


    def add_product_to_order(self, product: Product, count: int):
        try:
            line_product = self.products.get(product=product)
            line_product.count += count
            line_product.summ = line_product.count*product.actual_price
        except me.DoesNotExist:
            self.products.create(product=product, count=count, summ=count*product.actual_price)
        self.save()

    @classmethod
    def get_count_products_in_active_order(cls, user):
        sums = cls.objects(Q(user=user) and Q(status=Order.ORDER_ACTIVE)).aggregate([
            {'$unwind': '$products'},
            {'$group': {'_id': '$_id', 'count_products': {'$sum': '$products.count'}}}
            ])
        if sums.alive:
            elem = sums.next()
            return elem['count_products']
        else:
            return 0


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
    ORDER_PROCESSED = 'order_processed'
    ORDER_CANCELED = 'order_canceled'
    CURRENCY = 'currerncy'
    PCS = 'pcs'
    SUMM_TO_PAY = 'summ_to_pay'
    ORDER = 'order'
    FROM = 'from'
    ORDER_STATUS = 'order_status'


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
        (ORDER_HISTORY, 'order_history'),

        (ORDER_PROCESSED, 'order_processed'),
        (ORDER_CANCELED, 'order_canceled'),

        (CURRENCY, 'currerncy'),
        (PCS, 'pcs'),
        (SUMM_TO_PAY, 'summ_to_pay'),
        (ORDER, 'order'),
        (FROM, 'from'),
        (ORDER_STATUS, 'order_status')


    )
    title = me.StringField(required=True, choices=TITLES_CONSTANT, unique=True)
    body = me.StringField(min_length=2, max_length=4096)

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
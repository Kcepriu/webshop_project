from models import Category, Product

class InitialData:
    data_from_init = {'Category' :[
        ['Стекло', 'Стекляная посуда', None],
        ['Сервировка', 'Посуда для сервировки', None],
        ['Кондитерский инвентарь', 'Посуда для кондитеров', None],

        ['Барное стекло', 'Стекло для бара', 'Стекло'],
        ['Ресторанное стекло', 'Стакло для ресторанов', 'Стекло'],

        ['Чафиндиши и диспенсеры', 'Описание Чафиндиши и диспенсеры', 'Сервировка'],
        ['Стойки банкетные', 'Описание Стойки банкетные', 'Сервировка'],
        ['Блюда и крышки', 'Описание Блюда и крышки', 'Сервировка'],
        ['Корзины', 'Корзины для продуктов', 'Сервировка'],

        ['Формы для выпечки и десертов', 'Описание Формы для выпечки и десертов', 'Кондитерский инвентарь'],
        ['Формы для шоколада', 'Описание Формы для шоколада', 'Кондитерский инвентарь'],
        ['Формы для мороженого', 'Описание Формы для мороженого', 'Кондитерский инвентарь'],
        ['Формы для мастики', 'Описание Формы для мастики', 'Кондитерский инвентарь'],
    ],
        'Product': [
            {   'title': 'N4231 Стакан низкий',
                'description':'N4231 Стакан низкий 270 мл серия "Pop Corn"',
                'parameters': {
                    'height': 10, 'widht': 11, 'length': 12,'weight': 13
                },
                'in_stock': 50, 'is_available': True, 'price': 100, 'discount': 10,
                'category': 'Барное стекло'
            },
            {'title': '320267 Стакан высокий',
             'description': '320267 Стакан высокий 470 мл серия "Oriente" цвет голубой',
             'parameters': {
                 'height': 14,
                 'widht': 15,
                 'length': 16,
                 'weight': 17
             },
             'in_stock': 60,
             'is_available': True,
             'price': 110,
             'discount': 5,
             'category': 'Барное стекло'
             },

            {'title': 'N5082 Бокал для шампанского ',
             'description': 'N5082 Бокал для шампанского 230 мл серия "Vina Juliette"',
             'parameters': {
                 'height': 18,
                 'widht': 19,
                 'length': 20,
                 'weight': 21
             },
             'in_stock': 60,
             'is_available': True,
             'price': 150,
             'discount': 10,
             'category': 'Ресторанное стекло'
             },
            {'title': '335942 Кувшин с крышкой ',
             'description': '335942 Кувшин с крышкой 1,9 л серия "Romantic"',
             'parameters': {
                 'height': 11,
                 'widht': 12,
                 'length': 13,
                 'weight': 14
             },
             'in_stock': 0,
             'is_available': True,
             'price': 10,
             'discount': 0,
             'category': 'Ресторанное стекло'
             },

            {'title': '10865 Диспенсер',
             'description': '10865 Диспенсер для молока 6 л',
             'parameters': {
                 'height': 10, 'widht': 11, 'length': 12, 'weight': 13
             },
             'in_stock': 50, 'is_available': True, 'price': 100, 'discount': 10,
             'category': 'Чафиндиши и диспенсеры'
             },

            {'title': '82328-1 Мармит',
             'description': '82328-1 Марміт для перших страв, н/ж кришка, 10 л',
             'parameters': {
                 'height': 10, 'widht': 11, 'length': 12, 'weight': 13
             },
             'in_stock': 50, 'is_available': True, 'price': 100, 'discount': 10,
             'category': 'Чафиндиши и диспенсеры'
             },

            {'title': 'COD. 183 Подставка для торта "Мемфис" (d 30 cm)',
             'description': 'COD. 192 Підставка для торта',
             'parameters': {
                 'height': 10, 'widht': 11, 'length': 12, 'weight': 13
             },
             'in_stock': 50, 'is_available': True, 'price': 100, 'discount': 10,
             'category': 'Стойки банкетные'
             },
            {'title': '11623 Стойка банкетная',
             'description': '11623 Дерев''яний ящик-стійка GN 2/4, h-10.5 см',
             'parameters': {
                 'height': 10, 'widht': 11, 'length': 12, 'weight': 13
             },
             'in_stock': 50, 'is_available': True, 'price': 100, 'discount': 10,
             'category': 'Стойки банкетные'
             },
            {'title': '00969 Подставка из сланца d 28 см',
             'description': '00969 Дошка зі сланцю d 28 см',
             'parameters': {
                 'height': 10, 'widht': 11, 'length': 12, 'weight': 13
             },
             'in_stock': 50, 'is_available': True, 'price': 100, 'discount': 10,
             'category': 'Блюда и крышки'
             },
            {'title': '01317 Блюдо прямоугольное 39х26 см',
             'description': '01317 Блюдо прямокутне сервірувальне  39х26 см',
             'parameters': {
                 'height': 10, 'widht': 11, 'length': 12, 'weight': 13
             },
             'in_stock': 50, 'is_available': True, 'price': 100, 'discount': 10,
             'category': 'Блюда и крышки'
             },
            {'title': 'PERA & FICO 115 Форма для десерта "PERA & FICO" 115 мл х 5',
             'description': 'PERA & FICO 115   Форма силіконова 60 x 55 h 76 mm + підставка',
             'parameters': {
                 'height': 10, 'widht': 11, 'length': 12, 'weight': 13
             },
             'in_stock': 50, 'is_available': True, 'price': 100, 'discount': 10,
             'category': 'Формы для выпечки и десертов'
             },
            {'title': 'KIT CANDLE IN THE WIND Набор форм для десерта "Свеча на ветру"',
             'description': 'KIT CANDLE IN THE WIND Набір силіконових форм  250 x 80.5 h 95 mm - 3 шт.',
             'parameters': {
                 'height': 10, 'widht': 11, 'length': 12, 'weight': 13
             },
             'in_stock': 50, 'is_available': True, 'price': 100, 'discount': 10,
             'category': 'Формы для выпечки и десертов'
             },
            {'title': '1213 CW Модуль для шоколада "Ежикк" 52x38x23 мм, 12 шт. x24 г',
             'description': '1213 CW Форма для шоколаду "Їжачок" 52x38x23 мм,  12 шт. x24 г',
             'parameters': {
                 'height': 10, 'widht': 11, 'length': 12, 'weight': 13
             },
             'in_stock': 50, 'is_available': True, 'price': 100, 'discount': 10,
             'category': 'Формы для шоколада'
             },
            {'title': 'CHOCOBIGEV Фонтан для шоколада 3,5 л, d 380, h800',
             'description': 'CHOCOBIGEV Фонтан для шоколаду 3,5 л, d 380, h800',
             'parameters': {
                 'height': 10, 'widht': 11, 'length': 12, 'weight': 13
             },
             'in_stock': 50, 'is_available': True, 'price': 100, 'discount': 10,
             'category': 'Формы для шоколада'
             },
            {'title': 'SLK806 Форма для декора "бвбочка" 37х30 мм',
             'description': 'SLK806 Форма "метелик" d 40 мм',
             'parameters': {
                 'height': 10, 'widht': 11, 'length': 12, 'weight': 13
             },
             'in_stock': 50, 'is_available': True, 'price': 100, 'discount': 10,
             'category': 'Формы для мастики'
             },
            {'title': '40-W159S Набор штампов для мастики "Пчела" 3 шт. (20x21,',
             'description': '40-W159S Набір штампів "Бджілка" (3 шт.)',
             'parameters': {
                 'height': 10, 'widht': 11, 'length': 12, 'weight': 13
             },
             'in_stock': 50, 'is_available': True, 'price': 100, 'discount': 10,
             'category': 'Формы для мастики'
             }


        ]}

    def initial_data(self):
        pass
        # for category in self.data_from_init['Category']:
        #     parent = Category.objects.get(title=category[2]) if category[2] else None
        #     print(category[0],category[2],  parent)
        #     new_category = Category.objects.create(title=category[0], description=category[1], parent=parent)
        #
        # for category in Category.objects.filter(parent=None):
        #     for subcategories in Category.objects.filter(parent=category):
        #         category.subcategories.append(subcategories)
        #     category.save()
        # for product in self.data_from_init['Product']:
        #     category = Category.objects.get(title=product['category'])
        #     product['category']=category
        #     Product.objects.create(**product)




if __name__ == '__main__':
    init_data = InitialData()
    init_data.initial_data()
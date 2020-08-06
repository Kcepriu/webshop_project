from models import Category, Product, New

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
             }],
        'News':[{'title': 'На Киевщине открыли стрельбу возле остановки: пострадал 20-летняя девушка.',
                'text': '''В городе Обухов (Киевская область) неизвестный водитель на авто открыл стрельбу возле 
                остановки общественного транспорта, в результате чего пострадала 20-летняя девушка.
                Его уже задержали в Киеве. Об этом написала пресс-служба полиции Киевской области на своем сайте 
                (чтобы посмотреть фото, доскролльте до конца страницы).
                "В городе Обухов вечером (Вероятно, речь о 5 августа. – Ред.) неустановленный водитель на автомобиле 
                синего цвета совершил несколько хаотичных выстрелов возле остановки общественного транспорта. 
                В pезультате чего была травмирована девушка – продавец из киоска, которая выбежала на улицу на звуки 
                стрельбы", – говорится в сообщении.
                После этого мужчина скрылся в неизвестном направлении. А 20-летнюю пострадавшую доставили в больницу, 
                где ей диагностировали непроникающее ранения грудной клетки.
                Подозреваемого задержали в Киеве в порядке ст. 208 УПК Украины. Им оказался 33-летний житель столицы. 
                Во время задержания полиция изъяла у мужчины пистолет "Форт-12", патроны, разрешительные документы.
                "Как выяснилось, конфликт возник на светофоре между водителями двух автомобилей. Потом один из них во 
                время движения машины из хулиганских побуждений начал вести беспорядочную стрельбу в сторону автомобиля 
                своего оппонента. В результате этих неприцельных выстрелов пострадала девушка-продавец", – отметили в 
                полиции.
                По данному факту открыли уголовное производство по ч. 4 ст. 296 (Хулиганство) Уголовного кодекса 
                Украины. Санкция статьи предусматривает лишение свободы на срок от трех до семи лет. Решается вопрос 
                об объявлении подозрения мужчине. Меру пресечения для него изберет суд.
                Как сообщал OBOZREVATEL, в Киеве иностранку обвинили в том, что она расчленила мужчину и пыталась 
                сжечь части его тела.'''},

                {'title': 'Інформація про постраждалих українців на борту двох вантажних суден у потру Бейрута не підтверджується',
                 'text': '''Інформація про те, що серед постраждалих від вибуху в порту Бейрута є українці, котрі прибули в порт міста двома вантажними суднами, не підтверджується, заявив міністр закордонних справ України Дмитро Кулеба.
                "Була інформація, що на двох вантажних суднах, які прибули з України в порт Бейрута, перебували громадяни України, але наразі ця інформація не підтверджується. За нашими даними, екіпаж цих кораблів складався виключно з іноземців", - сказав Кулеба в четвер на брифінгу.
                Потужні вибухи пролунали 4 серпня в портовій зоні ліванської столиці - Бейрута. Вибуховою хвилею зруйновано величезну кількість будівель, вибито шибки та двері. Пошкоджено будівлю міжнародного аеропорту. Вибухову хвилю відчули навіть на Кіпрі.
                Повідомляється про понад 130 загиблих і близько 5 тис. потерпілих унаслідок лиха. 300 тис. городян лишилися без домівок, збитки від вибуху оцінюються щонайменше у $3 млрд.
                Влада Лівану заявила, що причиною потужних вибухів у портовій зоні Бейрута стали 2750 тонн аміачної селітри, що зберігалася на складі, конфіскованої митними службами шість років тому.
                5 серпня посол України в Лівані Ігор Осташ підтвердив інформацію, що серед серйозно постраждалих унаслідок вибухів у Бейруті громадян України немає. "Є деякі сім'ї, у яких постраждало майно, будинки, квартири. Є також незначні травми, порізи, забої (у громадян України - ІФ), але постраждалих серйозно поки що немає. Наразі йдеться про допомогу у відновленні будинків або квартир. На сьогодні серйозних проблем, пов'язаних із загрозою життя, для українців немає", - сказав Осташ в ефірі одного з українських телеканалів.
                Водночас він зазначив, що посольство намагається розшукати інформацію про нібито два українські кораблі, що розміщувалися в районі вибухів. Посол повідомив, що наразі є інформація, що серйозно постраждав корабель ООН, а стосовно українських громадян, українських моряків такої інформації немає.
                Дипломат також нагадав, що контакти посольства є на сайті дипломатичної місії. "Усі наші телефони є на сайті посольства. "Просто введіть "Посольство України в Лівані" - відразу побачите всі телефони гарячої лінії", - сказав Осташ.'''},

                {'title': 'Экс-директор «Центргаза» осужден на 8 лет за растрату более ₴8,5 млн.',
                 'text': '''Высший антикоррупционный суд признал виновным экс-директора дочернего предприятия «Центргаз» ОАО «Кировоградгаз» Константина Старовойта в растрате 8,6 млн гривен средств указанного предприятия и приговорил к 8 годам лишения свободы.
                Об этом УНН сообщает со ссылкой на пресс-службу ВАКС.
                ВАКС осудил на 8 лет экс-директора "Центргаза" за растрату более 8,5 млн гривен
                «Обвиняемому было назначено наказание в виде лишения свободы сроком на 8 лет с лишением права занимать должности, связанные с выполнением административно-хозяйственных функций, сроком на 3 года, а также с конфискацией части имущества», — говорится в сообщении.
                Сообщается, что судом установлено, что в июне 2017 года обвиняемый умышленно, злоупотребляя своим служебным положением, совершил растрату вверенного ему имущества в размере 8,6 млн грн в пользу другого юридического лица, в обогащении которого был заинтересован. Коллегия судей пришла к выводу, что с целью сокрытия своих преступных намерений экс-директор ГП «Центргаз» заключил договор на заведомо невыгодных условиях для возглавляемого им предприятия, что сделало невозможным его выполнение и повлекло выбытие денежных средств в размере 8,6 млн грн.'''},

                {'title': 'В Полтавской области мужчина угрожал подорвать собственную семью',
                 'text': '''В Полтавской области мужчина с предметом, похожим на самодельный боеприпас, угрожал подорвать собственную семью, сообщает пресс-служба полиции.
                "По информации, которую в полицию по телефону сообщили местные жители, мужчина предметом, похожим на боеприпас, угрожал жене и ее матери расправой", - говорится в сообщении.
                Полицейские, приехавшие на вызов, задержали мужчину и провели осмотр помещения и прилегающей территории. Так, полиция обнаружила предмет, похожий на самодельное взрывное устройство. Вероятный боеприпас направили на экспертизу. 
                Правоохранители продолжают устанавливать обстоятельства происшествия.
                Сведения о происшествии внесены в Единый реестр досудебных расследований по ст. 129 Уголовного кодекса Украины ("Угроза убийством"). Также решается вопрос внесения сведений по факту незаконного обращения с боеприпасами (ч. 1 ст. 263 Уголовного кодекса Украины). '''}
        ]
    }

    def initial_data(self):

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
        for new in self.data_from_init['News']:
            New.objects.create(**new)

        pass




if __name__ == '__main__':
    init_data = InitialData()
    init_data.initial_data()
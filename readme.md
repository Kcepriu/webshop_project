**Stack:**

-mongodb
-mongoenginge
-marhmallow
-Telebot
-flask
-flas-restful
-googlr cloud
-linux
-nginx
-gunicorn

**Modules**
-BD
-BOT
-REST API

**DB**
-Category
(title, description, subcategories, parent)
-Product
(title, description, parameters, in_stock, is_available, price, discount, category)
-Cart
-Customer
(telegram_id, name, adress, )
-Text
(title, body)

**TASKS 
**Tasks Lesson1**
1) Заполнить бд тестовыми данными
2) Реализовать в боте ответ на комманду /start, бот должен отвечать Inline клавиатурой из
всех доступных категорий (root (верхнего уровня)).
3) Подумать о применении колекции Text (Тянуть текст привествия оттуда).


**Tasks Lesson2**
1) Организовать навигационную клавиатуру (из кнопок шаблонов). Следующие кнопки:
1. Категории
2. Товары со скидкой
3. Новости

2) Предусмотреть логику нажатия на каждую кнопку
1. Кнопка "Категории" - бот должен отвечать Inline клавиатурой из
всех доступных категорий (root (верхнего уровня))
2. "Товары со скидкой" - инлайн клавиатура из товаров со скидкой
3. Выводить сообщение с последними тремя новостями (создать и описать колекцию новостей)

**tastk 3
3)
Переробити з текстових констант в виборку даних із бази
Поле картинки у продуктов
Для каждого продукта писать в чат
1. Его картинка
Описание
Кнопра с пивязкой 

При клике на кнопке категории выводить список всех доступных подкатегорий
Если нет подкатегорий, выволить продукті категории ()

LESS 4)

1) Зарегистрироватся на гугл клауде, создать екземпляр виртуальной машины (VPS)
1.1)OS - Ubunrtu 18.04
1.2) CPU - 1 ядро
1.3) ОЗУ - 2 гіга
1.4) диск 40 гігов
Регион - Европа

Разрешить http and https трафик

2) Описать методі сервиса для работы с продуктами
3) ОПИСАТЬ МОДЕЛБ ЮЗЕРА. Предусмотреть максимально информативную сущность 
4) подумать над моделью заказа/Корзины


less 5
1. Реализовать модель корзины/ заказа
2. В боту предоставить возможность джобавлять товарі в корзину и усуществлять заказі
2.1 в процесе оформдения заказа запрашивать номер телефона и имя. мохранять в базу
3. в боте добавить возможность просматривать историю заказом

less 6
1. rest api для манипуляций с юзерами, заказами і категориями (использовать BluePrint)
2. Реализовать кнопку Назад при работе с катеогриями
3. обезательно он должен быти запущен через вубхук




    


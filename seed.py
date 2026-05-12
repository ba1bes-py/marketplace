from app import app, db, Product, ProductImage

with app.app_context():
    db.session.query(ProductImage).delete()
    db.session.query(Product).delete()
    db.session.commit()

    cement = Product(
        name="Цемент М500",
        price=420,
        description="""
Высокопрочный цемент М500 для строительных и ремонтных работ.

Характеристики:
• Марка прочности: М500
• Вес мешка: 50 кг
• Тип: портландцемент
• Цвет: серый
• Морозостойкость: высокая

Подходит для:
• заливки фундамента
• стяжки пола
• кладочных работ
• бетонирования

Обеспечивает надежное сцепление и устойчивость к нагрузкам.
""",
        category="Стройматериалы"
    )
    cement.images = [
        ProductImage(image_url="/static/images/cem1.webp"),
        ProductImage(image_url="/static/images/cem2.webp"),
        ProductImage(image_url="/static/images/cem3.webp")
    ]

    screwdriver = Product(
        name="Шуруповерт",
        price=5600,
        description="""
Аккумуляторный шуруповерт для дома, ремонта и строительных работ.

Характеристики:
• Напряжение: 48V
• Тип аккумулятора: Li-Ion
• Количество скоростей: 2
• Максимальные обороты: 2600 об/мин
• Подсветка рабочей зоны: есть

Комплектация:
• 2 аккумулятора
• зарядное устройство
• кейс для хранения

Подходит для:
• сборки мебели
• монтажа гипсокартона
• сверления дерева и металла
""",
        category="Инструменты"
    )
    screwdriver.images = [
        ProductImage(image_url="/static/images/sh1.png"),
        ProductImage(image_url="/static/images/sh2.png"),
        ProductImage(image_url="/static/images/sh3.webp"),
        ProductImage(image_url="/static/images/sh4.webp"),
        ProductImage(image_url="/static/images/sh5.webp"),
        ProductImage(image_url="/static/images/sh6.webp")
    ]

    perforator = Product(
        name="Перфоратор",
        price=8900,
        description="""
Мощный перфоратор для сверления бетона, кирпича и камня.

Характеристики:
• Мощность: 2000 Вт
• Режимы работы: 3
• Тип патрона: SDS+
• Сила удара: 5 Дж
• Реверс: есть

Подходит для:
• демонтажных работ
• сверления бетона
• монтажа конструкций

Усиленный корпус снижает вибрацию и повышает надежность инструмента.
""",
        category="Инструменты"
    )
    perforator.images = [
        ProductImage(image_url="/static/images/p1.webp"),
        ProductImage(image_url="/static/images/p2.webp"),
        ProductImage(image_url="/static/images/p3.webp"),
        ProductImage(image_url="/static/images/p4.webp"),
        ProductImage(image_url="/static/images/p5.webp"),
        ProductImage(image_url="/static/images/p6.webp"),
        ProductImage(image_url="/static/images/p7.webp")
    ]

    paint = Product(
        name="Краска интерьерная",
        price=1350,
        description="""
Интерьерная водоэмульсионная краска для стен и потолков.

Характеристики:
• Цвет: белый матовый
• Объем: 10 л
• Основа: акриловая
• Время высыхания: 2 часа
• Расход: до 12 м²/л

Подходит для:
• кухни
• спальни
• гостиной
• офисных помещений

Образует ровное покрытие без разводов и запаха.
""",
        category="Отделка и ремонт"
    )
    paint.images = [
        ProductImage(image_url="/static/images/paint1.webp"),
        ProductImage(image_url="/static/images/paint2.webp"),
        ProductImage(image_url="/static/images/paint3.webp")
    ]

    grinder = Product(
        name="Болгарка",
        price=4700,
        description="""
Угловая шлифмашина для резки и шлифовки различных материалов.

Характеристики:
• Мощность: 1400 Вт
• Диаметр диска: 125 мм
• Скорость вращения: 11000 об/мин
• Защита от перегрева: есть

Подходит для:
• резки металла
• обработки плитки
• шлифовки поверхностей

Компактный корпус обеспечивает удобный хват и точность работы.
""",
        category="Инструменты"
    )
    grinder.images = [
        ProductImage(image_url="/static/images/gr1.webp"),
        ProductImage(image_url="/static/images/gr2.webp"),
        ProductImage(image_url="/static/images/gr3.webp")
    ]

    drill = Product(
        name="Дрель ударная",
        price=3900,
        description="""
Компактная ударная дрель для домашнего и профессионального использования.

Характеристики:
• Мощность: 850 Вт
• Максимальный диаметр сверления: 13 мм
• Режим удара: есть
• Регулировка оборотов: есть

Подходит для:
• сверления дерева
• бетона
• металла
• монтажных работ

Удобная прорезиненная ручка уменьшает нагрузку на кисть.
""",
        category="Инструменты"
    )
    drill.images = [
        ProductImage(image_url="/static/images/dr1.webp"),
        ProductImage(image_url="/static/images/dr2.webp"),
        ProductImage(image_url="/static/images/dr3.webp")
    ]

    bricks = Product(
        name="Кирпич облицовочный",
        price=32,
        description="""
Облицовочный кирпич для фасадных и декоративных работ.

Характеристики:
• Материал: керамика
• Размер: 250×120×65 мм
• Цвет: красный
• Морозостойкость: F100

Подходит для:
• облицовки фасадов
• строительства заборов
• декоративной кладки

Устойчив к влаге и перепадам температуры.
""",
        category="Стройматериалы"
    )
    bricks.images = [
        ProductImage(image_url="/static/images/br1.webp"),
        ProductImage(image_url="/static/images/br2.webp")
    ]

    plaster = Product(
        name="Штукатурка гипсовая",
        price=580,
        description="""
Гипсовая штукатурка для выравнивания стен и потолков.

Характеристики:
• Вес мешка: 30 кг
• Цвет: белый
• Время высыхания: 24 часа
• Толщина слоя: до 50 мм

Подходит для:
• внутренних помещений
• подготовки стен под покраску
• отделочных работ

Обеспечивает гладкую поверхность без трещин.
""",
        category="Стройматериалы"
    )
    plaster.images = [
        ProductImage(image_url="/static/images/pl1.webp"),
        ProductImage(image_url="/static/images/pl2.webp"),
        ProductImage(image_url="/static/images/pl3.webp")
    ]

    tiles = Product(
        name="Плитка керамическая",
        price=1450,
        description="""
Керамическая плитка для ванной комнаты и кухни.

Характеристики:
• Размер: 60×60 см
• Поверхность: матовая
• Влагостойкость: высокая
• Материал: керамика

Подходит для:
• ванной комнаты
• кухни
• прихожей

Современный дизайн и устойчивость к истиранию.
""",
        category="Отделка и ремонт"
    )
    tiles.images = [
        ProductImage(image_url="/static/images/tl1.webp"),
        ProductImage(image_url="/static/images/tl2.webp")
    ]

    wallpaper = Product(
        name="Обои виниловые",
        price=2200,
        description="""
Виниловые обои для современных интерьеров.

Характеристики:
• Тип: виниловые
• Ширина рулона: 1 м
• Длина рулона: 10 м
• Основа: флизелиновая

Подходит для:
• спальни
• гостиной
• офиса

Легко моются и устойчивы к механическим повреждениям.
""",
        category="Отделка и ремонт"
    )
    wallpaper.images = [
        ProductImage(image_url="/static/images/wp1.webp"),
        ProductImage(image_url="/static/images/wp2.webp"),
        ProductImage(image_url="/static/images/wp3.webp")
    ]

    db.session.add_all([
        cement,
        screwdriver,
        perforator,
        paint,
        grinder,
        drill,
        bricks,
        plaster,
        tiles,
        wallpaper
    ])

    db.session.commit()

    print("Товары и изображения добавлены в базу")
from flask import Flask, render_template, session, redirect, url_for, request, abort, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "my_secret_key_123"

database_url = os.getenv("DATABASE_URL")
print("DATABASE_URL FROM ENV:", database_url)
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

categories = ["Стройматериалы", "Инструменты", "Отделка и ремонт"]


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<User {self.email}>"
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Заполните все поля")
            return redirect(url_for("register"))

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Пользователь с такой почтой уже существует")
            return redirect(url_for("register"))

        new_user = User(
            email=email,
            password_hash=generate_password_hash(password)
        )

        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.id
        session["user_email"] = new_user.email

        return redirect(url_for("account"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash("Неверная почта или пароль")
            return redirect(url_for("login"))

        session["user_id"] = user.id
        session["user_email"] = user.email

        return redirect(url_for("account"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("user_email", None)

    return redirect(url_for("index"))


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)

    images = db.relationship(
        "ProductImage",
        backref="product",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Product {self.name}>"
    
class ProductImage(db.Model):
    __tablename__ = "product_images"

    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)

    def __repr__(self):
        return f"<ProductImage {self.image_url}>"


def get_product_by_id(product_id):
    return Product.query.get(product_id)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/catalog")
def catalog():
    selected_category = request.args.get("category")

    if selected_category and selected_category in categories:
        filtered_products = Product.query.filter_by(category=selected_category).all()
    else:
        filtered_products = Product.query.all()
        selected_category = None

    return render_template(
        "catalog.html",
        products=filtered_products,
        categories=categories,
        selected_category=selected_category
    )


@app.route("/product/<int:product_id>")
def product_page(product_id):
    product = get_product_by_id(product_id)

    if product is None:
        abort(404)

    return render_template("product.html", product=product)


@app.route("/add-to-cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    product = get_product_by_id(product_id)

    if product is None:
        abort(404)

    quantity = int(request.form.get("quantity", 1))

    cart = session.get("cart", {})

    product_id_str = str(product_id)
    cart[product_id_str] = cart.get(product_id_str, 0) + quantity

    session["cart"] = cart

    return redirect(url_for("cart"))


@app.route("/remove-from-cart/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]

    session["cart"] = cart
    return redirect(url_for("cart"))


@app.route("/account")
def account():
    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("account.html")


@app.route("/cart")
def cart():
    cart = session.get("cart", {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = get_product_by_id(int(product_id))

        if product:
            item_total = product.price * quantity
            cart_items.append({
                "product": product,
                "quantity": quantity,
                "item_total": item_total
            })
            total_price += item_total

    return render_template(
        "cart.html",
        cart_items=cart_items,
        total_price=total_price
    )

def seed_database():
    if Product.query.first():
        return

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

with app.app_context():
    db.create_all()
    seed_database()


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, session, redirect, url_for, request, abort, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "my_secret_key_123"

database_url = os.getenv("postgresql://marketplace_db_yiag_user:4wjBW9TO8Q0nWsatSFcxgx0XvTsuGbVk@dpg-d81dgrlckfvc738b6l5g-a/marketplace_db_yiag")

if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url or "postgresql://postgres:postgres@localhost:5432/marketplace?connect_timeout=3"
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

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
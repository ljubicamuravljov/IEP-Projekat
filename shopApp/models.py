from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()


class OrderProducts(database.Model):
    __tablename__ = "orderproducts"

    id = database.Column(database.Integer, primary_key=True)

    productId = database.Column(database.Integer, database.ForeignKey("product.id"), nullable=False)
    orderId = database.Column(database.Integer, database.ForeignKey("order.id"), nullable=False)
    quantity = database.Column(database.Integer, nullable=False)


class ProductCategories(database.Model):
    __tablename__ = "productcategories"

    id = database.Column(database.Integer, primary_key=True)
    productId = database.Column(database.Integer, database.ForeignKey("product.id"), nullable=False)
    categoryId = database.Column(database.Integer, database.ForeignKey("category.id"), nullable=False)

    def __repr__(self):
        return self.id


class Product(database.Model):
    __tablename__ = "product"

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(256), nullable=False, unique=True)
    price = database.Column(database.Float, nullable=False)

    categories = database.relationship("Category", secondary=ProductCategories.__table__, back_populates='products')
    orders = database.relationship("Order", secondary=OrderProducts.__table__, back_populates='products')

    def __repr__(self):
        return self.name


class Category(database.Model):
    __tablename__ = "category"

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(256), nullable=False)

    products = database.relationship("Product", secondary=ProductCategories.__table__, back_populates='categories')

    def __repr__(self):
        return self.name


class Order(database.Model):
    __tablename__ = "order"

    id = database.Column(database.Integer, primary_key=True)

    price = database.Column(database.Float, nullable=False, default=0)
    status = database.Column(database.String(8), nullable=False, default="CREATED")
    timestamp = database.Column(database.DateTime, nullable=False)
    userEmail = database.Column(database.String(256), nullable=False)
    address = database.Column(database.String(256))
    products = database.relationship("Product", secondary=OrderProducts.__table__, back_populates='orders')

from extensions import db
from datetime import datetime
from flask_login import UserMixin
from extensions import bcrypt

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Enum('admin', 'customer', name='user_roles'), nullable=False, default='customer')
    orders = db.relationship('Order', backref='user', lazy=True)

    def __repr__(self):
        return f'User {self.username} with role {self.role}'
    
    def set_as_admin(self):
        self.role = 'admin'
        db.session.commit()

    @property
    def is_admin(self):
        return self.role == 'admin'
    
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    table_number = db.Column(db.Integer, nullable=False)
    order_items = db.relationship('OrderItem', backref='order', lazy=True)
    status = db.Column(db.String(50), nullable=False, default='Pending')

    def __repr__(self):
        return f'Order for table number {self.table_number}'


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'OrderItem {self.id} for Order {self.order_id}'


class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    order_items = db.relationship('OrderItem', backref='menu_item', lazy=True)
    image = db.Column(db.String(100), nullable=False, default='default.png')
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    def __repr__(self):
        return f'MenuItem {self.name}'


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    menu_items = db.relationship('MenuItem', backref='category', cascade="all, delete", lazy=True)

    def __repr__(self):
        return f'Category {self.name}'


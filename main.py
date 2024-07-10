import flet as ft
from flet import Page, ElevatedButton, Column, Row, Text, TextField, Container, Card, ListView, ListTile, Divider, Dropdown
from models import MenuItem, User, Category
from app import create_app
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user
from extensions import db

app = create_app()
bcrypt = Bcrypt(app)

def main(page: Page):
    cart = []
    notification_text = Text("")  # Notification text component

    def load_menu_items(category_id=None):
        with app.app_context():
            if category_id:
                menu_items = MenuItem.query.filter_by(category_id=category_id).all()
            else:
                menu_items = MenuItem.query.all()
            menu_list.controls.clear()
            for item in menu_items:
                menu_list.controls.append(
                    ListTile(
                        title=Text(item.name),
                        subtitle=Text(item.description),
                        trailing=Text(f"Price: {item.price}"),
                        on_click=lambda e, item=item: add_to_cart(item)
                    )
                )
                menu_list.controls.append(Divider())
            page.update()

    def load_categories():
        with app.app_context():
            categories = Category.query.all()
            category_dropdown.options = [cat.name for cat in categories]
            page.update()

    def add_to_cart(menu_item):
        cart.append(menu_item)
        cart_list.controls.append(
            ListTile(
                title=Text(menu_item.name),
                trailing=Text(f"Price: {menu_item.price}"),
            )
        )
        page.update()

    def show_home(e):
        content.controls.clear()
        content.controls.append(Text("Welcome to YummYum", size=32, weight="bold"))
        page.update()

    def show_about(e):
        content.controls.clear()
        content.controls.append(Text("About YummYum", size=32, weight="bold"))
        page.update()

    def show_menu(e):
        load_menu_items()
        content.controls.clear()
        content.controls.append(
            Column([
                Text("Menu", size=24),
                Row([
                    Text("Filter by category"),
                    Dropdown(options=[], on_change=lambda e: load_menu_items(e.target.value))
                ]),
                menu_list
            ])
        )
        load_categories()  # Load categories initially
        page.update()

    def show_register(e):
        def register_user(e):
            with app.app_context():
                username = username_field.value
                email = email_field.value
                password = password_field.value
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                user = User(username=username, email=email, password=hashed_password)
                db.session.add(user)
                db.session.commit()
                notification_text.value = "User registered successfully!"
                page.update()
        
        content.controls.clear()
        username_field = TextField(label="Username")
        email_field = TextField(label="Email")
        password_field = TextField(label="Password", password=True)
        content.controls.append(
            Column([
                Text("Register", size=24),
                username_field,
                email_field,
                password_field,
                ElevatedButton("Register", on_click=register_user),
                notification_text  # Display notification here
            ])
        )
        page.update()

    def show_login(e):
        def login_user_func(e):
            with app.app_context():
                email = email_field.value
                password = password_field.value
                user = User.query.filter_by(email=email).first()
                if user and bcrypt.check_password_hash(user.password, password):
                    login_user(user)
                    notification_text.value = "Login successful!"
                else:
                    notification_text.value = "Login failed!"
                page.update()

        content.controls.clear()
        email_field = TextField(label="Email")
        password_field = TextField(label="Password", password=True)
        content.controls.append(
            Column([
                Text("Login", size=24),
                email_field,
                password_field,
                ElevatedButton("Login", on_click=login_user_func),
                notification_text  # Display notification here
            ])
        )
        page.update()

    def show_cart(e):
        content.controls.clear()
        content.controls.append(
            Column([
                Text("Cart", size=24),
                cart_list,
                ElevatedButton("Place Order", on_click=place_order)
            ])
        )
        page.update()

    def place_order(e):
        with app.app_context():
            # Add logic to place order
            notification_text.value = "Order placed successfully!"
            cart.clear()
            cart_list.controls.clear()
            page.update()

    page.title = "Restaurant Management System"

    menu_list = ListView(controls=[])
    cart_list = ListView(controls=[])
    category_dropdown = Dropdown(options=[])

    nav = Column([
        ElevatedButton("Home", on_click=show_home),
        ElevatedButton("About", on_click=show_about),
        ElevatedButton("Menu", on_click=show_menu),
        ElevatedButton("Register", on_click=show_register),
        ElevatedButton("Login", on_click=show_login),
        ElevatedButton("Cart", on_click=show_cart),
    ])

    content = Column()

    show_home(None)  # Initial page load

    page.add(Row([nav, content]))

ft.app(target=main)
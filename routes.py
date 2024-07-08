from flask import render_template, request, redirect, url_for, flash, Blueprint
from models import User, Order, OrderItem, MenuItem, Category
from forms import OrderForm, RegistrationForm, LoginForm, MenuItemForm
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from flask_login import LoginManager
from werkzeug.utils import secure_filename
import os


bcrypt = Bcrypt()
bp = Blueprint("main", __name__)


def register_routes(app, db):
    @app.route("/")
    @app.route("/home")
    def home():
        return render_template("home.html", restaurant_name="YummYum")

    @app.route("/about")
    def about():
        return render_template("about.html", restaurant_name="YummYum")

    @app.route("/menu")
    def menu():
        category_id = request.args.get('category_id', type=int)
        if category_id:
            menu_items = MenuItem.query.filter_by(category_id=category_id).all()
        else:
            menu_items = MenuItem.query.all()
        categories = Category.query.all()
        return render_template(
            "menu.html", menu_items=menu_items,
            categories=categories,
            selected_category_id=category_id,
            restaurant_name="YummYum"
        )

    @app.route("/create_order", methods=["GET", "POST"])
    def create_order():
        form = OrderForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                new_order = Order(
                    email=form.email.data, table_number=form.table_number.data
                )
                db.session.add(new_order)
                db.session.commit()
                return redirect(url_for("order_details") )
            else:
                flash("User ID does not exist.")
        return render_template("create_order.html", form=form)

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for("home"))
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
                "utf-8"
            )
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=hashed_password,
            )
            db.session.add(user)
            db.session.commit()
            flash(
                "Your account has been created! You are now able to log in.", "success"
            )
            return redirect(url_for("login"))
        return render_template("register.html", title="Register", form=form)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("home"))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember_me.data)
                flash("Login successful!", "success")
                return redirect(url_for("home"))
            else:
                flash("Login unsuccessful. Please check email and password.", "danger")
        return render_template("login.html", title="Login", form=form)

    @app.route("/logout")
    def logout():
        logout_user()
        return redirect(url_for("home"))

    @app.route("/menu/new", methods=["GET", "POST"])
    def new_menu_item():
        form = MenuItemForm()
        if form.validate_on_submit():

            menu_item = MenuItem(
                name=form.name.data,
                description=form.description.data,
                price=form.price.data,
                category_id=form.category.data,
            )

            image = form.image.data
            # If no image is provided, use the default image
            if not image:
                image = app.config["DEFAULT_IMAGE"]

            # Handle image upload if provided
            else:
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                image.save(image_path)
                menu_item.image = filename
            # Save filename to database or process as needed

            db.session.add(menu_item)
            db.session.commit()
            flash("Menu item has been created!", "success")
            return redirect(url_for("menu"))
        return render_template(
            "create_menu_item.html", title="New Menu Item", form=form
        )

    @app.route("/menu/<int:item_id>/update", methods=["GET", "POST"])
    @login_required
    def update_menu_item(item_id):
        menu_item = MenuItem.query.get_or_404(item_id)
        form = MenuItemForm(obj=menu_item)

        if form.validate_on_submit():
            # Update basic fields
            menu_item.name = form.name.data
            menu_item.description = form.description.data
            menu_item.price = form.price.data
            menu_item.category_id = form.category.data

            # Handle image upload
            image = form.image.data
            if image and hasattr(image, "filename"):
                # If an image is provided, process it
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                image.save(image_path)
                menu_item.image = filename
            elif not menu_item.image:
                # If no image is provided and no existing image, use the default image
                menu_item.image = app.config["DEFAULT_IMAGE"]

            db.session.commit()
            flash("Menu item has been updated!", "success")
            return redirect(url_for("menu"))  # Redirect to the menu page after update

        elif request.method == "GET":
            # Populate the form fields with existing data
            form.name.data = menu_item.name
            form.description.data = menu_item.description
            form.price.data = menu_item.price
            form.category.data = menu_item.category_id

        return render_template(
            "create_menu_item.html",
            title="Update Menu Item",
            form=form,
            legend="Update Menu Item",
        )


    @app.route("/menu/<int:item_id>/delete", methods=["POST"])
    @login_required
    def delete_menu_item(item_id):
        menu_item = MenuItem.query.get_or_404(item_id)
    
        if request.method == 'POST':
            db.session.delete(menu_item)
            db.session.commit()
            flash('Menu item has been deleted!', 'success')
            return redirect(url_for('menu'))  # Redirect to menu page after deletion
        else:
            flash('Failed to delete menu item.', 'error')
            return redirect(url_for('menu'))  # Redirect to menu page if not POST request
        
    @bp.route("/add_category", methods=["GET", "POST"])
    def add_category():
        if request.method == "POST":
            category_name = request.form["category_name"]
            # Check if category already exists
            existing_category = Category.query.filter_by(name=category_name).first()
            if existing_category is None:
                new_category = Category(name=category_name)
                db.session.add(new_category)
                db.session.commit()
                flash("Category added successfully!", "success")
            else:
                flash("Category already exists.", "danger")
            return redirect(url_for("main.add_category"))
        return render_template("add_category.html")
        
    @app.route('/categories/<int:category_id>/delete', methods=['POST'])
    @login_required
    def delete_category(category_id):
        category = Category.query.get_or_404(category_id)
        
        # Handle associated menu items
        for item in category.menu_items:
            db.session.delete(item)
        
        db.session.delete(category)
        db.session.commit()
        flash('Category has been deleted!', 'success')
        return redirect(url_for('menu'))
    
    @app.route('/order_details', methods=['GET', 'POST'])
    def order_details():
        # Fetch all orders with their associated user and order items
        orders_with_details = (
            db.session.query(Order, User, OrderItem, MenuItem)
            .join(User, Order.email == User.email)
            .join(OrderItem, Order.id == OrderItem.order_id)
            .join(MenuItem, OrderItem.menu_item_id == MenuItem.id)
            .all()
        )
        orders_dict = {}
        for order, user, order_item, menu_item in orders_with_details:
            if order.id not in orders_dict:
                orders_dict[order.id] = {
                    'order_id': order.id,
                    'username': user.username,
                    'order_created_at': order.created_at,
                    'table_number': order.table_number,
                    'items': [],
                    'total_price': 0
                }
            item_detail = {
                'menu_item_name': menu_item.name,
                'menu_item_description': menu_item.description,
                'menu_item_price': menu_item.price,
                'quantity': order_item.quantity,
                'item_total': menu_item.price * order_item.quantity
            }
            orders_dict[order.id]['items'].append(item_detail)
            orders_dict[order.id]['total_price'] += item_detail['item_total']

        # Convert the dictionary to a list for easier templating
        orders_list = list(orders_dict.values())
        return render_template('orders.html', orders=orders_list)

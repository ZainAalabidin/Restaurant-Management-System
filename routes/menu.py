from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import OrderItem, MenuItem, Category
from werkzeug.utils import secure_filename
from forms import MenuItemForm
from extensions import db
import os

menu_bp = Blueprint('menu', __name__)

@menu_bp.route("/menu")
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

@menu_bp.route("/menu/new", methods=["GET", "POST"])
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
            image = os.getenv("DEFAULT_IMAGE")
        # Handle image upload if provided
        else:
            filename = secure_filename(image.filename)
            image_path = os.path.join(os.getenv("UPLOAD_FOLDER"), filename)
            image.save(image_path)
            menu_item.image = filename
        # Save filename to database or process as needed
        db.session.add(menu_item)
        db.session.commit()
        flash("Menu item has been created!", "success")
        return redirect(url_for("menu.menu"))
    return render_template(
        "create_menu_item.html", title="New Menu Item", form=form
    )
@menu_bp.route("/menu/<int:item_id>/update", methods=["GET", "POST"])
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
            image_path = os.path.join(os.getenv("UPLOAD_FOLDER"), filename)
            image.save(image_path)
            menu_item.image = filename
        elif not menu_item.image:
            # If no image is provided and no existing image, use the default image
            menu_item.image = os.getenv("DEFAULT_IMAGE")
        db.session.commit()
        flash("Menu item has been updated!", "success")
        return redirect(url_for("menu.menu"))  # Redirect to the menu page after update
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
@menu_bp.route("/menu/<int:item_id>/delete", methods=["POST"])
@login_required
def delete_menu_item(item_id):
    menu_item = MenuItem.query.get_or_404(item_id)
    # Find and delete related order items
    order_items = OrderItem.query.filter_by(menu_item_id=item_id).all()
    for order_item in order_items:
        db.session.delete(order_item)

    if request.method == 'POST':
        db.session.delete(menu_item)
        db.session.commit()
        flash('Menu item has been deleted!', 'success')
        return redirect(url_for('menu.menu'))  # Redirect to menu page after deletion
    else:
        flash('Failed to delete menu item.', 'error')
        return redirect(url_for('menu.menu'))  # Redirect to menu page if not POST request
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import OrderItem, MenuItem, Category
from werkzeug.utils import secure_filename
from forms import MenuItemForm
from extensions import db
import os

# Create a blueprint for menu-related routes
menu_bp = Blueprint('menu', __name__)

# Route to display menu items, optionally filtered by category
@menu_bp.route("/menu")
def menu():
    # Get the category ID from the query parameters
    category_id = request.args.get('category_id', type=int)
    # Filter menu items by category if category_id is provided
    if category_id:
        menu_items = MenuItem.query.filter_by(category_id=category_id).all()
    else:
        menu_items = MenuItem.query.all()
    # Fetch all categories for category filtering
    categories = Category.query.all()
    
    # Redirect to the admin dashboard (seems unintended here)
    redirect(url_for("admin.admin_dashboard"))
    
    # Render the menu page with menu items, categories, and selected category
    return render_template(
        "menu.html", menu_items=menu_items,
        categories=categories,
        selected_category_id=category_id,
        restaurant_name="YummYum"
    )

# Route to create a new menu item
@menu_bp.route("/menu/new", methods=["GET", "POST"])
def new_menu_item():
    form = MenuItemForm()
    if form.validate_on_submit():
        # Create a new menu item with form data
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
        else:
            # Handle image upload if provided
            filename = secure_filename(image.filename)
            image_path = os.path.join(os.getenv("UPLOAD_FOLDER"), filename)
            image.save(image_path)
            menu_item.image = filename
        
        # Add new menu item to the database
        db.session.add(menu_item)
        db.session.commit()
        flash("Menu item has been created!", "success")
        return redirect(url_for("admin.admin_dashboard"))
    
    # Render the form for creating a new menu item
    return render_template(
        "create_menu_item.html", title="New Menu Item", form=form
    )

# Route to update an existing menu item
@menu_bp.route("/menu/<int:item_id>/update", methods=["GET", "POST"])
@login_required
def update_menu_item(item_id):
    menu_item = MenuItem.query.get_or_404(item_id)
    form = MenuItemForm(obj=menu_item)
    if form.validate_on_submit():
        # Update the menu item with form data
        menu_item.name = form.name.data
        menu_item.description = form.description.data
        menu_item.price = form.price.data
        menu_item.category_id = form.category.data
        
        image = form.image.data
        if image and hasattr(image, "filename"):
            # Process and save the new image if provided
            filename = secure_filename(image.filename)
            image_path = os.path.join(os.getenv("UPLOAD_FOLDER"), filename)
            image.save(image_path)
            menu_item.image = filename
        elif not menu_item.image:
            # If no new image is provided and no existing image, use the default image
            menu_item.image = os.getenv("DEFAULT_IMAGE")
        
        # Commit the changes to the database
        db.session.commit()
        flash("Menu item has been updated!", "success")
        return redirect(url_for("admin.admin_dashboard"))  # Redirect to admin dashboard after update
    elif request.method == "GET":
        # Prepopulate the form with existing data
        form.name.data = menu_item.name
        form.description.data = menu_item.description
        form.price.data = menu_item.price
        form.category.data = menu_item.category_id
    
    # Render the form for updating a menu item
    return render_template(
        "create_menu_item.html",
        title="Update Menu Item",
        form=form,
        legend="Update Menu Item",
    )

# Route to delete a menu item
@menu_bp.route("/menu/<int:item_id>/delete", methods=["POST"])
@login_required
def delete_menu_item(item_id):
    menu_item = MenuItem.query.get_or_404(item_id)
    # Find and delete related order items
    order_items = OrderItem.query.filter_by(menu_item_id=item_id).all()
    for order_item in order_items:
        db.session.delete(order_item)
    
    if request.method == 'POST':
        # Delete the menu item from the database
        db.session.delete(menu_item)
        db.session.commit()
        flash('Menu item has been deleted!', 'success')
        return redirect(url_for('menu.menu'))  # Redirect to menu page after deletion
    else:
        flash('Failed to delete menu item.', 'error')
        return redirect(url_for("admin.admin_dashboard"))  # Redirect to admin dashboard if not POST request

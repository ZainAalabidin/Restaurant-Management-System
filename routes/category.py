from flask import render_template, request, redirect, url_for, flash, Blueprint
from models import Category, OrderItem
from flask_login import login_required
from extensions import db

# Create a blueprint for category-related routes
category_bp = Blueprint('category', __name__)

# Route to add a new category
@category_bp.route("/add_category", methods=["GET", "POST"])
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
        return redirect(url_for("category.add_category"))
    return render_template("add_category.html")

# Route to delete a category
@category_bp.route('/categories/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    
    # Handle associated menu items
    for item in category.menu_items:
        # Find and delete related order items
        order_items = OrderItem.query.filter_by(menu_item_id=item.id).all()
        for order_item in order_items:
            db.session.delete(order_item)
        db.session.delete(item)
    
    db.session.delete(category)
    db.session.commit()
    flash('Category has been deleted!', 'success')
    return redirect(url_for('menu.menu'))

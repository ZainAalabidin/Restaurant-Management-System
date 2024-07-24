from flask import Blueprint, render_template, flash, url_for, redirect
from flask_login import login_required, current_user
from models import Order, MenuItem, Category

# Create a blueprint for the admin routes
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    # Check if the current user is an admin
    if not current_user.is_admin:
        # Flash a warning message if the user is not authorized
        flash('You are not authorized to access the admin dashboard.', 'warning')
        # Redirect to a non-admin page if the user is not authorized
        return redirect(url_for('home.home'))
    
    # Fetch data for the admin dashboard, e.g., orders, menu items, categories
    orders = Order.query.all()
    menu_items = MenuItem.query.all()
    categories = Category.query.all()
    
    # Render the admin dashboard template with the fetched data
    return render_template('dashboard.html', orders=orders, menu_items=menu_items, categories=categories)

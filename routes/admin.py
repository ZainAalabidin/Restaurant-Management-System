from flask import Blueprint, render_template, flash, url_for, redirect
from flask_login import login_required, current_user
from models import Order, MenuItem, Category

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('You are not authorized to access the admin dashboard.', 'warning')
        return redirect(url_for('home.home'))  # Redirect to a non-admin page if not authorized
    
    # Fetch data for the admin dashboard, e.g., orders, menu items, categories
    orders = Order.query.all()
    menu_items = MenuItem.query.all()
    categories = Category.query.all()
    
    return render_template('dashboard.html', orders=orders, menu_items=menu_items, categories=categories)

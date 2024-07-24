from flask import render_template, Blueprint, redirect, url_for, flash, request
from models import User, Order, OrderItem, MenuItem
from extensions import db
from flask_login import current_user, login_required

order_bp = Blueprint('order', __name__)

# Route to display the details of a specific order
@order_bp.route('/order_details/<int:order_id>', methods=['GET'])
def order_details(order_id):
    # Query to get order details along with related user, order items, and menu items
    order_with_details = (
        db.session.query(Order, User, OrderItem, MenuItem)
        .join(User, Order.user_id == User.id)
        .join(OrderItem, Order.id == OrderItem.order_id)
        .join(MenuItem, OrderItem.menu_item_id == MenuItem.id)
        .filter(Order.id == order_id)
        .all()
    )

    # Check if order exists
    if not order_with_details:
        return "Order not found", 404

    # Prepare order details for rendering
    order_dict = {
        'order_id': order_with_details[0][0].id,
        'username': order_with_details[0][1].username,
        'order_created_at': order_with_details[0][0].created_at,
        'table_number': order_with_details[0][0].table_number,
        'items': [],
        'total_price': 0
    }

    # Populate the order items and calculate total price
    for order, user, order_item, menu_item in order_with_details:
        item_detail = {
            'menu_item_name': menu_item.name,
            'menu_item_description': menu_item.description,
            'menu_item_price': menu_item.price,
            'quantity': order_item.quantity,
            'item_total': menu_item.price * order_item.quantity
        }
        order_dict['items'].append(item_detail)
        order_dict['total_price'] += item_detail['item_total']

    # Render order details template
    return render_template('order_details.html', order=order_dict)

# Route to display a list of all orders
@order_bp.route('/orders', methods=['GET'])
def orders():
    if not current_user.is_admin:
        flash('You are not authorized to access this page.', 'warning')
        return redirect(url_for('home.home'))

    # Query to get all orders along with related user, order items, and menu items
    orders_with_details = (
        db.session.query(Order, User, OrderItem, MenuItem)
        .join(User, Order.user_id == User.id)
        .join(OrderItem, Order.id == OrderItem.order_id)
        .join(MenuItem, OrderItem.menu_item_id == MenuItem.id)
        .all()
    )

    # Prepare orders data for rendering
    orders_dict = {}
    for order, user, order_item, menu_item in orders_with_details:
        if order.id not in orders_dict:
            orders_dict[order.id] = {
                'order_id': order.id,
                'username': user.username,
                'order_created_at': order.created_at,
                'table_number': order.table_number,
                'items': [],
                'total_price': 0.0
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

    # Convert orders dictionary to a list for rendering
    orders_list = list(orders_dict.values())
    return render_template('orders.html', orders=orders_list)

# Route to update the status of a specific order
@order_bp.route('/update_order_status/<int:order_id>', methods=['POST'])
@login_required
def update_order_status(order_id):
    if not current_user.is_admin:
        flash('You are not authorized to perform this action.', 'warning')
        return redirect(url_for('home.home'))

    status = request.form.get('status')
    order = Order.query.get_or_404(order_id)
    order.status = status
    db.session.commit()
    flash('Order status updated successfully.', 'success')
    return redirect(url_for('order.orders'))

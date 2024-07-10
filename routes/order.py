#order.py
from flask import render_template, Blueprint
from models import User, Order, OrderItem, MenuItem
from extensions import db

order_bp = Blueprint('order', __name__)

@order_bp.route('/order_details/<int:order_id>', methods=['GET'])
def order_details(order_id):
    # Fetch the order with its associated user and order items
    order_with_details = (
        db.session.query(Order, User, OrderItem, MenuItem)
        .join(User, Order.email == User.email)
        .join(OrderItem, Order.id == OrderItem.order_id)
        .join(MenuItem, OrderItem.menu_item_id == MenuItem.id)
        .filter(Order.id == order_id)
        .all()
    )

    if not order_with_details:
        return "Order not found", 404

    order_dict = {
        'order_id': order_with_details[0][0].id,
        'username': order_with_details[0][1].username,
        'order_created_at': order_with_details[0][0].created_at,
        'table_number': order_with_details[0][0].table_number,
        'items': [],
        'total_price': 0
    }

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

    return render_template('order_details.html', order=order_dict)

@order_bp.route('/orders', methods=['GET'])
def orders():
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

    orders_list = list(orders_dict.values())
    return render_template('orders.html', orders=orders_list)
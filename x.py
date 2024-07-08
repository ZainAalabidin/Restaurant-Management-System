from flask import render_template, request

from models import User, Order, OrderItem, MenuItem


def register_routes(app, db):
    @app.route('/')
    def index():
        # Fetch all orders with their associated user and order items
        orders_with_details = (
            db.session.query(Order, User, OrderItem, MenuItem)
            .join(User, Order.user_id == User.id)
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

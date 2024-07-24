from flask import render_template, request, redirect, url_for, flash, Blueprint, session
from models import User, Order, OrderItem, MenuItem
from forms import OrderForm
from extensions import db

# Create a blueprint for cart-related routes
cart_bp = Blueprint('cart', __name__)

# Route to add an item to the cart
@cart_bp.route("/add_to_cart/<int:item_id>", methods=["GET", "POST"])
def add_to_cart(item_id):
    menu_item = MenuItem.query.get_or_404(item_id)
    cart = session.get('cart', [])
    
    # Check if the item is already in the cart
    for item in cart:
        if item['id'] == menu_item.id:
            flash(f'{menu_item.name} is already in your cart!', 'info')
            return redirect(url_for('menu.menu'))
    
    # Add the item to the cart
    cart.append({
        'id': menu_item.id,
        'name': menu_item.name,
        'price': menu_item.price,
        'quantity': 1
    })
    session['cart'] = cart
    flash(f'Added {menu_item.name} to your cart!', 'success')
    return redirect(url_for('menu.menu'))

# Route to view the cart
@cart_bp.route("/view_cart", methods=["GET", "POST"])
def view_cart():
    form = OrderForm()
    cart = session.get('cart', [])

    # Calculate the total price
    total_price = sum(item['price'] * item['quantity'] for item in cart)

    if form.validate_on_submit():
        user_id = form.user_id.data
        table_number = form.table_number.data
        user = User.query.filter_by(id=user_id).first()

        if user:
            # Create a new order
            new_order = Order(user_id=user_id, table_number=table_number)
            db.session.add(new_order)
            db.session.commit()

            # Add items to the order
            for item in cart:
                new_order_item = OrderItem(order_id=new_order.id, menu_item_id=item['id'], quantity=item['quantity'])
                db.session.add(new_order_item)

            db.session.commit()

            # Clear the cart
            session.pop('cart', None)
            flash('Order placed successfully!', 'success')
            return redirect(url_for("order.order_details", order_id=new_order.id))
        else:
            flash("User does not exist.", "danger")
    
    return render_template("view_cart.html", cart=cart, form=form, total_price=total_price)

# Route to update the quantity of an item in the cart
@cart_bp.route("/update_cart/<int:item_id>", methods=["POST"])
def update_cart(item_id):
    new_quantity = int(request.form.get('quantity'))
    cart = session.get('cart', [])
    
    # Update the quantity of the specified item
    for item in cart:
        if item['id'] == item_id:
            item['quantity'] = new_quantity
            break
    
    session['cart'] = cart
    return redirect(url_for('cart.view_cart'))

# Route to remove an item from the cart
@cart_bp.route("/remove_from_cart/<int:item_id>", methods=['POST'])
def remove_from_cart(item_id):
    cart = session.get('cart', [])
    
    # Remove the specified item from the cart
    for item in cart:
        if item['id'] == item_id:
            cart.remove(item)
            break
    
    session['cart'] = cart
    flash('Item removed from cart', 'success')
    return redirect(url_for('cart.view_cart'))

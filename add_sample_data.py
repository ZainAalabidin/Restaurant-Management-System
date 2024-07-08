# add_sample_data.py
from app import app, db
from models import Category, MenuItem

with app.app_context():
    db.create_all()

    # Add categories
    categories = [
        Category(name='Appetizers'),
        Category(name='Main Courses'),
        Category(name='Desserts'),
        Category(name='Beverages')
    ]

    db.session.add_all(categories)
    db.session.commit()

    # Add menu items
    menu_items = [
        MenuItem(name='Spring Rolls', description='Crispy rolls with vegetables', price=5.99, image='spring_rolls.jpg', category_id=8),
        MenuItem(name='Chicken Curry', description='Spicy chicken curry with rice', price=12.99, image='chicken_curry.jpg', category_id=9),
        MenuItem(name='Cheesecake', description='Creamy cheesecake with strawberry topping', price=6.99, image='cheesecake.jpg', category_id=11),
        MenuItem(name='Lemonade', description='Refreshing lemonade', price=2.99, image='lemonade.jpg', category_id=10)
    ]

    db.session.add_all(menu_items)
    db.session.commit()

    print("Sample data added!")

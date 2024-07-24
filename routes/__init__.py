def register_routes(app, db, bcrypt):
    # Import blueprints from different modules
    from .home import home_bp
    from .auth import auth_bp
    from .menu import menu_bp
    from .cart import cart_bp
    from .category import category_bp
    from .order import order_bp
    from .admin import admin_bp

    # Register each blueprint with the Flask application instance
    app.register_blueprint(home_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(admin_bp)

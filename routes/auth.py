from flask import render_template, redirect, url_for, flash, Blueprint, request
from flask_login import login_user, current_user, logout_user
from forms import RegistrationForm, LoginForm, UpdateProfileForm
from flask_login import login_required
from extensions import db, bcrypt
from models import User, Order

# Create a blueprint for authentication routes
auth_bp = Blueprint("auth", __name__)

# Route for user registration
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    # Redirect to home if the user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for("home.home"))
    
    # Initialize the registration form
    form = RegistrationForm()
    
    # Validate the form submission
    if form.validate_on_submit():
        # Hash the user's password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        
        # Create a new user instance
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
        )
        
        # Add the new user to the database
        db.session.add(user)
        db.session.commit()
        
        # Flash a success message and redirect to the login page
        flash("Your account has been created! You are now able to log in.", "success")
        return redirect(url_for("auth.login"))
    
    # Render the registration template
    return render_template("register.html", title="Register", form=form)

# Route for user login
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # Redirect to home if the user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for("home.home"))
    
    # Initialize the login form
    form = LoginForm()
    
    # Validate the form submission
    if form.validate_on_submit():
        # Query the user by email
        user = User.query.filter_by(email=form.email.data).first()
        
        # Check the password and log in the user if valid
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("Login successful!", "success")
            return redirect(url_for("home.home"))
        else:
            flash("Login unsuccessful. Please check email and password.", "danger")
    
    # Render the login template
    return render_template("login.html", title="Login", form=form)

# Route for user profile update
@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    # Initialize the profile update form
    form = UpdateProfileForm()
    
    # Validate the form submission
    if form.validate_on_submit():
        # Update orders table if the email is changed
        if current_user.email != form.email.data:
            orders = Order.query.filter_by(user_id=current_user.id).all()
            for order in orders:
                order.username = form.username.data
            db.session.commit()

        # Update the current user's details
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.password.data:
            current_user.set_password(form.password.data)
        db.session.commit()
        
        # Flash a success message and redirect to the profile page
        flash("Your account has been updated!", "success")
        return redirect(url_for("auth.profile"))
    
    # Pre-fill the form with the current user's data when the page is first loaded
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    # Render the profile template
    return render_template("profile.html", title="Profile", form=form)

# Route for user logout
@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home.home"))

# Route to promote a user to admin
@auth_bp.route("/users/<int:user_id>/promote_to_admin", methods=["GET", "POST"])
@login_required
def promote_to_admin(user_id):
    # Check if the current user is an admin
    if not current_user.is_admin:
        flash("You are not authorized to perform this action.", "warning")
        return redirect(url_for("home.home"))
    
    # Get the user by ID and promote to admin
    user = User.query.get_or_404(user_id)
    user.set_as_admin()
    flash(f"{user.username} has been promoted to admin.", "success")
    return redirect(url_for("admin.admin_dashboard"))

# Example of a protected route
@auth_bp.route("/some_protected_route")
def some_protected_route():
    # Check if the current user is authenticated and an admin
    if current_user.is_authenticated and current_user.is_admin:
        return render_template("admin_dashboard.html", "orders.html")
    else:
        return "Access Denied", 403

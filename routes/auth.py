from flask import render_template, redirect, url_for, flash, Blueprint, request
from flask_login import login_user, current_user, logout_user
from forms import RegistrationForm, LoginForm, UpdateProfileForm
from flask_login import login_required
from extensions import db, bcrypt
from models import User, Order

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
        )
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", title="Register", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("Login successful!", "success")
            return redirect(url_for("home.home"))
        else:
            flash("Login unsuccessful. Please check email and password.", "danger")
    return render_template("login.html", title="Login", form=form)


@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if current_user.email != form.email.data:
            # Update orders table to match the new email
            orders = Order.query.filter_by(id=current_user.id).all()
            for order in orders:
                order.username = form.username.data
            db.session.commit()

        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.password.data:
            current_user.set_password(form.password.data)
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("auth.profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("profile.html", title="Profile", form=form)


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home.home"))


@auth_bp.route("/users/<int:user_id>/promote_to_admin", methods=["GET", "POST"])
@login_required
def promote_to_admin(user_id):
    if not current_user.is_admin:
        flash("You are not authorized to perform this action.", "warning")
        return redirect(url_for("home.home"))

    user = User.query.get_or_404(user_id)
    user.set_as_admin()
    flash(f"{user.username} has been promoted to admin.", "success")
    return redirect(url_for("admin.admin_dashboard"))


@auth_bp.route("/some_protected_route")
def some_protected_route():
    if current_user.is_authenticated and current_user.is_admin():
        return render_template("admin_dashboard.html", "orders.html")
    else:
        return "Access Denied", 403

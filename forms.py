from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, PasswordField, BooleanField, TextAreaField, FloatField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange, Optional
from models import User, Category
from flask_wtf.file import FileField
from flask_login import current_user


# Define Registration Form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        # Custom validator to check if the email is already in use
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different email.')

# Define Login Form 
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

# Define Menu Item Form
class MenuItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    image = FileField('Image', validators=[Optional()])
    submit = SubmitField('Save')

    def __init__(self, *args, **kwargs):
        # Initialize the form and set the choices for the category field
        super(MenuItemForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name) for category in Category.query.all()]

# Define Order Form
class OrderForm(FlaskForm):
    user_id = StringField('User ID', validators=[DataRequired()])
    table_number = IntegerField('Table Number', validators=[DataRequired()])
    submit = SubmitField('Create Order')

# Define Update Profile Form
class UpdateProfileForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])
    submit = SubmitField('Update')

    def validate_email(self, email):
        # Custom validator to check if the email is already in use, excluding the current user's email
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length, Email

class Register_Form(FlaskForm):
    """Form for registering new user"""
    name = StringField('Username', validators=[InputRequired(), Length(max=20, message='Username is too long (max 20 chars)')])

    password = PasswordField('Password', validators=[InputRequired()])

    email = StringField('Email', validators=[InputRequired(), Length(max=50, message='Email is too long (max 50 chars)'), Email(message='Invalid Email')])

    first_name = StringField('First Name', validators=[InputRequired(), Length(max=30, message='First Name is too long (max 30 chars)')])

    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=30, message='Last Name is too long (max 30 chars)')])

class Login_Form(FlaskForm):
    name = StringField('Username', validators=[InputRequired()])

    password = PasswordField('Password', validators=[InputRequired()])

class Feedback_Form(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(max=100, message='Title is too long (max 100 chars)')])

    content = TextAreaField('Content', validators=[InputRequired()], render_kw = {'rows':5, 'cols':50})
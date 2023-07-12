from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from models import db, connect_db, User
from forms import Register_Form, Login_Form


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

@app.route('/')
def show_home():
    return redirect('/register')

@app.route('/register', methods=['GET','POST'])
def register():
    """Show the registration form and handle the post request"""
    form = Register_Form()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(name, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()
        session['cur_user'] = new_user.username
        return redirect('/secret')

    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    """Show the login form and handle the post request"""
    form = Login_Form()
    if form.validate_on_submit():
        username = form.name.data
        password = form.password.data
        user = User.login(username,password)
        if user:
            session['cur_user'] = user.username
            flash("Successfully logged in!")
            return redirect('/secret')
        else:
            flash("Invalid username/password!")
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)

@app.route('/secret', methods=['GET'])
def show_secret():
    """Show the secret page if a user is logged in, otherwise redirect back to home"""
    if session.get('cur_user'):
        return render_template('secret.html')
    else:
        flash("You must register and/or login to view that page!")
        return redirect('/register')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('cur_user')
    flash("Successfully logged out!")
    return redirect('/login')

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from models import db, connect_db, User, Feedback
from forms import Register_Form, Login_Form, Feedback_Form
import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

@app.route('/')
def show_home():
    feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).limit(5).all()
    return render_template('home.html',feedbacks=feedbacks)

#=====================================================================================================
@app.route('/register', methods=['GET','POST'])
def register():
    """Show the registration form and handle the post request"""
    if session.get('cur_user'):
        flash("You are already logged in!")
        return redirect('/')
    else:
        form = Register_Form()
        if form.validate_on_submit():
            name = form.name.data
            if User.query.filter_by(username=name).first():
                flash("That username is already taken!")
                return redirect('/register')
            else:
                password = form.password.data
                email = form.email.data
                if User.query.filter_by(email=email).first():
                    flash("That email is already taken!")
                    return redirect('/register')
                else:
                    first_name = form.first_name.data
                    last_name = form.last_name.data
                    new_user = User.register(name, password, email, first_name, last_name)
                    db.session.add(new_user)
                    db.session.commit()
                    session['cur_user'] = new_user.username
                    return redirect(f'/users/{new_user.username}')
        else:
            return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    """Show the login form and handle the post request"""
    if session.get('cur_user'):
        flash("You are already logged in!")
        return redirect('/')
    else:
        form = Login_Form()
        if form.validate_on_submit():
            username = form.name.data
            password = form.password.data
            user = User.login(username,password)
            if user:
                session['cur_user'] = user.username
                flash("Successfully logged in!")
                return redirect(f'/users/{user.username}')
            else:
                flash("Invalid username/password!")
                return render_template('login.html', form=form)
        else:
            return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('cur_user')
    flash("Successfully logged out!")
    return redirect('/login')

@app.route('/users/<string:username>')
def show_user(username):
    """Shows information about a user
    Also validates that they are logged in as themselves"""
    if session.get('cur_user') == username:
        user = User.query.filter_by(username=username).first()
        feedbacks = Feedback.query.filter_by(username=username).order_by(Feedback.created_at.desc()).all()
        return render_template('user.html',user=user, feedbacks=feedbacks)
    else:
        flash('You must be logged in as the correct user to see that page!')
        return redirect('/register')

@app.route('/users/<string:username>/delete')
def delete_user(username):
    """Validates and deletes the user with their posts"""
    if session.get('cur_user')==username:
        user = User.query.filter_by(username=username).first()
        db.session.delete(user)
        db.session.commit()
        flash("Account successfully deleted!")
        session.pop('cur_user')
        return redirect('/')
    else:
        flash('You must be logged in as the correct user to see that page!')
        return redirect('/login')

@app.route('/users/<string:username>/delete/confirm')
def show_confirm_delete(username):
    """Validates and shows a page confirming if the user wants to delete their profile"""
    if session.get('cur_user')==username:
        return render_template('delete.html', username=username)
    else:
        flash('You must be logged in as the correct user to see that page!')
        return redirect('/login')

#=====================================================================================================
@app.route('/users/<string:username>/feedback/add', methods = ['GET','POST'])
def add_feedback(username):
    """Shows the form for adding feedback and process the post request
    Also validates the user is logged in correctly"""
    if session.get('cur_user') == username:
        form = Feedback_Form()
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            new_feedback = Feedback(title=title, content=content, username=username)
            db.session.add(new_feedback)
            db.session.commit()
            return redirect(f'/users/{username}')
        else:
            return render_template('add.html',form=form)
    else:
        flash('You must be logged in as the correct user to see that page!')
        return redirect('/login')

@app.route('/feedback/<int:feedback_id>/update',methods = ['GET','POST'])
def update_feedback(feedback_id):
    """Shows the edit form and handles the post request
    Also validates the user"""
    feedback = Feedback.query.get(feedback_id)
    if session.get('cur_user')==feedback.username:
        form  = Feedback_Form(obj=feedback)
        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            feedback.created_at = datetime.datetime.now()
            db.session.add(feedback)
            db.session.commit()
            return redirect(f'/users/{feedback.username}')
        else:
            return render_template('update.html',form=form)
    else:
        flash('You must be logged in as the correct user to see that page!')
        return redirect('/login')

@app.route('/feedback/<int:feedback_id>/delete',methods=['POST'])
def delete_feedback(feedback_id):
    """Deletes a specified feedback with validation"""
    feedback = Feedback.query.get(feedback_id)
    if session.get('cur_user')==feedback.username:
        db.session.delete(feedback)
        db.session.commit()
    else:
        flash('You must be logged in as the correct user to see that page!')
        return redirect('/login')

#=====================================================================================================
@app.route('/secret', methods=['GET'])
def show_secret():
    """Show the secret page if a user is logged in, otherwise redirect back to home"""
    if session.get('cur_user'):
        return render_template('secret.html')
    else:
        flash("You must register and/or login to view that page!")
        return redirect('/register')
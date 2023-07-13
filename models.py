from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import datetime

bcrypt = Bcrypt()

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User"""
    __tablename__ = 'users'

    username = db.Column(db.String(20), primary_key=True, unique=True)

    password = db.Column(db.Text, nullable=False)

    email = db.Column(db.String(50), nullable=False, unique=True)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    feedbacks = db.Relationship('Feedback', cascade='all, delete-orphan')

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register a user with a hashed password"""
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode('utf8')
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def login(cls,username, password):
        """Login a user by checking the hashed passwords
        
        Returns user if true, otherwise returns false"""
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

#==============================================================================================

class Feedback(db.Model):
    """Feedback"""
    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(100), nullable=False)

    content = db.Column(db.Text, nullable=False)

    username = db.Column(db.Text, db.ForeignKey('users.username'))

    created_at = db.Column(db.DateTime, nullable=False, default = datetime.datetime.now)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
db = SQLAlchemy()
class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    username=db.Column(db.String(80),unique=True,nullable=False)
    password=db.Column(db.String(200),nullable=False)
    role=db.Column(db.String(20),nullable=False)
    approvals=db.Column(db.Boolean,default=False)
    phone=db.Column(db.String(20))
class Opportunity(db.Model):
    __tablename__='opportunities'
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    max_volunteers = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='open')
    participation_date=db.Column(db.DateTime, nullable=False)
class Booking(db.Model):
    __tablename__='bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunities.id'), nullable=False)
    cancelled = db.Column(db.Boolean, default=False)
    booking_date=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
class Category(db.Model):
    __tablename__='categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
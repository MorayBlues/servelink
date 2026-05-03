from app import app, db
from models import User

with app.app_context():
    user = User.query.filter_by(username='winyou').first()
    if user:
        user.approvals = True
        db.session.commit()
        print('Organization approved')
    else:
        print('User not found')
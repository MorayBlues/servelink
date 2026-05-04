from models import User
from flask_bcrypt import Bcrypt
from app import app, db
bcrypt = Bcrypt(app)

with app.app_context():
    admin = User(
        name='Admin',
        email='admin@servelink.com',
        username='admin',
        password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
        role='admin',
        approvals=True
    )
    db.session.add(admin)
    db.session.commit()
    print('Admin created')
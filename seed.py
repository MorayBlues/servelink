from models import User, Category
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
with app.app_context():
    categories=['Education', 'Food & Hunger', 'Health','Community']
    for name in categories:
        cat = Category(name=name)
        db.session.add(cat)
    db.session.commit() 
    print('admin created')
    print('Categories added')       
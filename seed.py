from app import app, db
from models import Opportunity, Category
from datetime import datetime

with app.app_context():
    cat = Category(name='Environment')
    db.session.add(cat)
    db.session.commit()
    
    opp = Opportunity(
        organization_id=1,
        title='Beach Cleanup',
        description='Help clean Nairobi dam area',
        location='Nairobi',
        max_volunteers=5,
        category_id=1,
        status='open',
        participation_date=datetime(2026, 6, 1)
    )
    db.session.add(opp)
    db.session.commit()
    print('Done')
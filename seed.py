from models import User, Category, Opportunity
from flask_bcrypt import Bcrypt
from app import app, db
from datetime import datetime
bcrypt = Bcrypt(app)

with app.app_context():

    cat1= Category(name='Environment')
    cat2= Category(name='Education')
    cat3= Category(name='Health')
    cat4= Category(name='Community')
    cat5= Category(name='Food & Hunger')
    db.session.add_all([cat1, cat2, cat3, cat4, cat5])
    db.session.commit() 

    admin = User(
        name='Admin',
        email='admin@servelink.com',
        username='admin',
        password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
        role='admin',
        approvals=True
    )
    org1= User(
        name='Ngong Hills Volunteers',
        email='info@ngonghillsvolunteers.org',
        username='ngonghills',
        password=bcrypt.generate_password_hash('Password1').decode('utf-8'),
        role='organization',
        approvals=True,
        phone='0712345678'
    )

    org2= User(
        name='PACEMaker International',
        email='info@pacemakerinternational.org',
        username='pacemakerINT',
        password=bcrypt.generate_password_hash('Password2').decode('utf-8'),
        role='organization',
        approvals=True,
        phone='0723456789'
    )

    org3= User(
        name='Amref Health Africa',
        email='info@amrefhealthafrica.org',
        username='amrefhealth_Africa',
        password=bcrypt.generate_password_hash('Password3').decode('utf-8'),
        role='organization',
        approvals=True,
        phone='0734567890'
    )

    org4= User(
        name='Community Kenya voluntary and community development',
        email='info@communitykenyacommunitydevelopment.org',
        username='CKVCD',
        password=bcrypt.generate_password_hash('Password4').decode('utf-8'),
        role='organization',
        approvals=True,
        phone='0745678901'
    )

    org5= User(
        name='Shining Hope For Communities',
        email='info@shininghope.org',
        username='shininghope',
        password=bcrypt.generate_password_hash('Password5').decode('utf-8'),
        role='organization',
        approvals=True,
        phone='0756789012'
    )
    db.session.add(admin)
    db.session.add_all([org1, org2, org3, org4, org5])
    db.session.commit()
    print('admin created') 
    print('organizations added')

    opp1= Opportunity(
        organization_id=org1.id,
        title='Karura Forest Cleanup',
        description="Let's make Karura clean",
        location='Karura Forest',
        max_volunteers='45',
        category_id= cat1.id,
        status='open',
        participation_date=datetime(2026, 5, 25)
    )

    opp2= Opportunity(
        organization_id=org2.id,
        title='Teaching Future Generations',
        description="Help teach and mentor young children",
        location='Nairobi',
        max_volunteers='30',
        category_id= cat2.id,
        status='open',
       participation_date=datetime(2026, 6, 15) 
    )

    opp3= Opportunity(
        organization_id=org3.id,
        title='Medical camps',
        description="Participate in the Community outreach Program",
        location='Kibera',
        max_volunteers='15',
        category_id= cat3.id,
        status='open',
        participation_date=datetime(2026, 7, 10)
    )

    opp4= Opportunity(
        organization_id=org4.id,
        title='Building Kenels',
        description="Building Shelter for Homeless Dogs",
        location='Mathare',
        max_volunteers='53',
        category_id= cat4.id,
        status='open',
         participation_date=datetime(2026, 7, 5)
    )

    opp5= Opportunity(
        organization_id=org5.id,
        title='Feeding The Homeless',
        description="Help Give food to the street families",
        location='Ngara',
        max_volunteers='20',
        category_id= cat5.id,
        status='open',
         participation_date=datetime(2026, 8, 1)
    )
 
    db.session.add_all([opp1, opp2, opp3, opp4, opp5])
    db.session.commit() 
    print('Opportunities Created')     
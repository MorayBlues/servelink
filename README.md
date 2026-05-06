# ServeLink — Community Volunteering Platform

ServeLink connects volunteers with community service opportunities 
posted by local organizations. Admins manage approvals and platform integrity.

## Tech Stack
- Python 3.13 + Flask
- SQLAlchemy + SQLite
- Flask-Mail (Gmail SMTP)
- Flask-Bcrypt
- python-dotenv

## Setup & Run Locally

git clone <your-repo-url>
cd service-booking-platform2
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python reset_db.py
python seed.py
python app.py

Visit http://127.0.0.1:5000

## Environment Variables
Create a .env file with:
SECRET_KEY=your-secret-key
MAIL_USERNAME=your-gmail
MAIL_PASSWORD=your-app-password

## Demo Credentials
1.Admin
username='admin',
password='admin123'
2.Ngong Hills Volunteers
username='ngonghills',
password='Password1'
3.PACEMaker International
username='pacemakerINT',
password='Password2'
4.Amref Health Africa
username='amrefhealth_Africa',
password='Password3'
5.Community Kenya voluntary and community development
username='CKVCD',
password='Password4'
6.Shining Hope For Communities
username='shininghope',
password='Password5'
7.Shantel Mwangi
username='ShantyM',
password='Shantel23'
## Features
- Role-based auth (Volunteer, Organization, Admin)
- Organization approval flow
- Opportunity creation and admin approval
- Booking system with race condition protection
- Email notifications
- Responsive mobile UI
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from models import  db, User, Opportunity, Booking, Category
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///servelink.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY']='dev-secret-key'
bcrypt = Bcrypt(app)
db.init_app(app)
@app.route('/')
def home():
        return render_template('home.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        if User.query.filter_by(email=email).first():
             flash('Email already registered')
             return redirect(url_for('register'))
        if User.query.filter_by(username=username).first():
             flash('Username already taken')
             return redirect(url_for('register'))
        password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(name=name, email=email, username=username, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            if user.role == 'organization'and not user.approvals:
                flash('Your account is pending approval. Please wait for admin approval.')
                return redirect(url_for('login'))
            elif user.role == 'admin': 
             flash('Admin login successful!')
             return redirect(url_for('admin_dashboard'))
            elif user.role == 'volunteer':
              flash('Volunteer login successful!') 
              return redirect(url_for('volunteer_dashboard'))
            elif user.role == 'organization':
              flash('Organization login successful!')
              return redirect(url_for('organization_dashboard'))    
        else:
         flash('Invalid username or password')
         return redirect(url_for('login'))       
@app.route('/volunteer_dashboard')
def volunteer_dashboard():
    if 'user_id' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))
    if session['role'] != 'volunteer':
        flash('Access denied')
        return redirect(url_for('home'))
    locations = [loc[0] for loc in db.session.query(Opportunity.location).distinct()]
    dates = [opp.participation_date for opp in Opportunity.query.filter_by(status='open').all()]
    categories = Category.query.all()
    query = Opportunity.query.filter_by(status='open')
    category_id=request.args.get('category_id')
    if category_id:
        query = query.filter_by(category_id=category_id)
        flash(f'Filtering by category: {category_id}')
    elif 'category_id' in request.args:
        flash('No category filter applied')
    participation_date=request.args.get('participation_date')
    if participation_date:
        query = query.filter(Opportunity.participation_date >= participation_date)
        flash(f'Filtering by participation date: {participation_date}')
    elif 'participation_date' in request.args:
        flash('No participation date filter applied')     
    location=request.args.get('location')
    if location:
        query = query.filter_by(location=location)
        flash(f'Filtering by location: {location}')
    elif 'location' in request.args:
        flash('No location filter applied')
    my_bookings = Booking.query.filter_by(user_id=session['user_id'], cancelled=False).all()    
    opportunities = query.all()
    slots_remaining={}
    for opp in opportunities:
        booked=Booking.query.filter_by(opportunity_id=opp.id).count()
        slots_remaining[opp.id]=opp.max_volunteers-booked    
    return render_template('volunteer_dashboard.html', opportunities=opportunities, slots_remaining=slots_remaining, locations=locations, dates=dates, categories=categories, my_bookings=my_bookings)
@app.route('/book', methods=['POST'])
def book():
    if 'user_id' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))
    if session['role'] != 'volunteer':
        flash('Access denied')
        return redirect(url_for('home'))
    opportunity_id = request.form.get('opportunity_id')
    opportunity = Opportunity.query.with_for_update().get(opportunity_id)
    if not opportunity or opportunity.status != 'open':
        flash('Opportunity not available for booking.')
        return redirect(url_for('volunteer_dashboard'))
    booked_count = Booking.query.filter_by(opportunity_id=opportunity_id).count()
    if booked_count >= opportunity.max_volunteers:
        flash('No slots available for this opportunity.')
        return redirect(url_for('volunteer_dashboard'))
    existing_booking = Booking.query.filter_by(user_id=session['user_id'], opportunity_id=opportunity_id).first()
    if existing_booking and not existing_booking.cancelled:
        flash('You have already booked this opportunity.')
        return redirect(url_for('volunteer_dashboard'))
    elif existing_booking and existing_booking.cancelled:
       existing_booking.cancelled = False
       db.session.commit()
       flash('Booking reactivated successfully!')
       return redirect(url_for('volunteer_dashboard'))
    else:
        new_booking = Booking(user_id=session['user_id'], opportunity_id=opportunity_id)
        db.session.add(new_booking)
        db.session.commit()
        flash('Booking successful!')
        return redirect(url_for('volunteer_dashboard'))
@app.route('/cancel', methods=['POST'])
def cancel():
    if 'user_id' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))
    if session['role'] != 'volunteer':
        flash('Access denied')
        return redirect(url_for('home'))
    booking_id = request.form.get('booking_id')
    booking = Booking.query.get(booking_id)
    if not booking or booking.user_id != session['user_id']:
        flash('Booking not found.')
        return redirect(url_for('volunteer_dashboard'))
    booking.cancelled = True
    db.session.commit()
    flash('Booking cancelled successfully.')
    return redirect(url_for('volunteer_dashboard'))
@app.route('/organization_dashboard')
def organization_dashboard():
    if 'user_id' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))
    if session['role'] != 'organization':
        flash('Access denied')
        return redirect(url_for('home'))
    return 'organization dashboard - coming soon'
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))
    if session['role'] != 'admin':
        flash('Access denied')
        return redirect(url_for('home'))
    return 'admin dashboard - coming soon'
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('home'))        
if __name__ == '__main__':
    with app.app_context():
     db.create_all()
    app.run(debug=True) 

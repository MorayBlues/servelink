from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User
from flask_bcrypt import Bcrypt
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
    return 'volunteer dashboard - coming soon'
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

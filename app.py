from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import random
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
db_path = os.path.join(os.getcwd(), 'instance', 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    response = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

# College information database
college_data = {
    "admission": [
        "1. Admissions are open from June 1st to July 31st.2. You can apply online through our college website.\n"
        "2. You can apply online through our college website.\n"
        "3. Required documents: 10th/12th marksheets, transfer certificate, and ID proof."
    ],
    "courses": [
        "We offer BCA in Computer Science, BBA, BCOM, and MCOM.",
        "Postgraduate courses include MCOM in Finance and Accountants.",
        "We also offer MBA and MCA programs."
    ],
    "fees": [
        "Annual fees for BCA is ₹60,000.<br/>",
        "Annual fees for BBA is ₹50,000.",
        "Annual fees for BCOM is ₹40,000.",
        "Annual fees for MCOM is ₹60,000.",
        "Hostel fees is ₹80,000 per year including meals.",
        "Scholarships are available for meritorious students."
    ],
    "facilities": [
        "Campus has Wi-Fi, library, sports complex, and labs. 24/7 security and medical facilities available. Separate hostels for boys and girls with AC/non-AC options."
    ],
    "placement": [
        "Last year's placement rate was 92% with highest package of ₹12 LPA. Top recruiters include Infosys, ByJus, AllDigi and TCS. We have a dedicated placement cell for training and interviews."
    ],
    "contact": [
        "Email: bbcbellary@gmail.com <br/>",
        "Phone: Office, Administration & University Related Mr. Umashankar Ph: +91 9108816166, Mr. Naresh Reddy Ph: +91 9880862710<br/>",
        "Address: Siruguppa Road, Ballari Business College, Karnataka State - 560001"
    ],
    "result": [
        "You can check your result on our official UUCMS login website."
    ],
    "about bca": [
        "Bachelor of Computer Applications (BCA) at Basavarajeshwari Group of Institutions..."
    ],
    "about bba": [
        "Bachelor of Business Administration (BBA) at Basavarajeshwari Group of Institutions..."
    ],
    "about bcom": [
        "Bachelor of Commerce (B.Com) at Basavarajeshwari Group of Institutions..."
    ],
    "about mcom": [
        "Master of Commerce (M.Com) at Basavarajeshwari Group of Institutions..."
    ],
    "events & culture": [
        "We have a vibrant campus life with various events and activities."
    ],
    "home": [
        "Welcome to Ballari Business College Enquiry Chatbot..!"
    ],
    "bcafee": [
        "Annual fees for BCA is ₹60,000.Even Scholarships are provided for merit students."
    ],
    "bbafee": [
        "Annual fees for BBA is ₹50,000.Even Scholarships are provided for merit students."
    ],
    "bcomfee": [
        "Annual fees for BCOM is ₹40,000.Even Scholarships are provided for merit students."
    ]
}

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password. Please try again or register.', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))
        
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists!', 'danger')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/home')
def home():
    if 'user_id' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('login'))
    return render_template('home.html', username=session['username'])

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if 'user_id' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        message = request.form['message']
        response = generate_response(message.lower())
        
        chat = ChatHistory(
            user_id=session['user_id'],
            message=message,
            response=response
        )
        db.session.add(chat)
        db.session.commit()
        
        return jsonify({'response': response})
    
    return render_template('chatbot.html')

def generate_response(message):
    responses = []
    
    if any(word in message for word in ['hello', 'hi', 'hey']):
        responses.append("Hello! How can I assist you with your college enquiry today?")
    
    if 'admission' in message:
        responses.extend(college_data['admission'])
    if 'course' in message or 'program' in message:
        responses.extend(college_data['courses'])
    if 'fee' in message or 'payment' in message:
        responses.extend(college_data['fees'])
    if 'facility' in message or 'hostel' in message:
        responses.extend(college_data['facilities'])
    if 'placement' in message or 'job' in message:
        responses.extend(college_data['placement'])
    if 'contact' in message or 'address' in message:
        responses.extend(college_data['contact'])
    if 'about bca' in message or 'bca' in message:
        responses.extend(college_data['about bca'])
    if 'about bba' in message or 'bba' in message:
        responses.extend(college_data['about bba'])
    if 'about bcom' in message or 'bcom' in message:
        responses.extend(college_data['about bcom'])
    if 'about mcom' in message or 'mcom' in message:
        responses.extend(college_data['about mcom'])
    if 'result' in message or 'marks' in message:
        responses.extend(college_data['result'])
    if 'home' in message or 'about' in message:
        responses.extend(college_data['home'])
    if 'bca1' in message or '1' in message:
        responses.extend(college_data['bcafee'])
    if 'bba2' in message or '2' in message:
        responses.extend(college_data['bbafee'])
    if 'bcom3' in message or '3' in message:
        responses.extend(college_data['bcomfee'])
    
    if not responses:
        responses = [
            "I'm sorry, I didn't understand that. Could you rephrase your question?",
            "I'm here to help with college enquiries. You can ask about admissions, courses, fees, etc.",
            "Could you provide more details about your query?"
        ]
    
    return "\n".join(responses)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

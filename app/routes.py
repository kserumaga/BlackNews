from flask import Flask, render_template, request, redirect, url_for, flash, session
from app.models.user_model import User, authenticate_user
from app.config import SUPABASE_URL, SUPABASE_KEY  # Import configuration
from supabase import create_client

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Use a secure key in production

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = authenticate_user(email, password)
    
    if user:
        session['user_id'] = user['id']
        flash('Login successful!', 'success')
        if user.get('admin_level') == 1:
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('index'))
    else:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        response = supabase.table('user_profile').select('*').eq('email', email).execute()
        if response.data:
            flash('Invalid password', 'danger')
        else:
            flash('Email not found', 'danger')
        
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/admin')
def admin_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Fetch user from database
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    response = supabase.table('user_profile').select('*').eq('id', session['user_id']).execute()
    user = response.data[0] if response.data else None

    if not user or not user.get('is_admin'):
        flash('Access denied', 'danger')
        return redirect(url_for('index'))

    # Fetch all users for management
    users_response = supabase.table('user_profile').select('*').execute()
    users = users_response.data if users_response.data else []

    return render_template('admin_dashboard.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
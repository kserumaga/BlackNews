from flask import Flask, render_template, request, redirect, url_for, flash, session
from app.models.user_model import User

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Use a secure key in production

@app.route('/')
def landing_page():
    return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Authenticate user
        user = authenticate_user(email, password)
        if user:
            session['user_id'] = user['id']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

def authenticate_user(email, password):
    # Implement authentication logic
    # Example: Fetch user from database and verify password
    return None

if __name__ == '__main__':
    app.run(debug=True)
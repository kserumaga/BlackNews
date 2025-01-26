from flask import Flask, render_template, request, redirect, url_for, flash, session
from app.models.user_model import User, authenticate_user

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
        return redirect(url_for('index'))
    else:
        flash('Invalid credentials', 'danger')
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
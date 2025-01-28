from flask import Flask, render_template, request, redirect, url_for, flash, session, abort, Blueprint
from flask_login import login_required, current_user, login_user, logout_user
from app.user_model import User
from app.config import Config
from supabase import create_client
from app.services.access_control import update_user_role
from flask import current_app
from app.services.supabase import supabase
import re
from app.news.news import NewsService

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Use a secure key in production

print(dir(User))  # Add this temporarily in routes.py before login route as a test of the login


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('landing.html')

@main_bp.route('/home')
@login_required
def home():
    """Authenticated user's dashboard"""
    try:
        # Get featured articles
        featured = NewsService.get_featured_articles(2)
        
        # Get recent articles
        recent = NewsService.get_recent_articles(4)
        
        return render_template('home.html',
            featured_articles=featured,
            recent_articles=recent
        )
    
    except Exception as e:
        current_app.logger.error(f"Home error: {str(e)}")
        return render_template('error.html', error="Could not load articles"), 500

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        if not email or not password:
            flash('Both email and password are required', 'danger')
            return redirect(url_for('main.login'))
        
        user = User.authenticate(email, password)
        if user:
            login_user(user, remember=True)
            flash('Login successful', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('auth/login.html')

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('main.home'))

@main_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@main_bp.route('/admin')
def admin_dashboard():
    return render_template('admin/dashboard.html')

@main_bp.route('/admin/feature/<article_id>')
@login_required
def feature_article(article_id):
    if not current_user.is_admin:
        abort(403)
        
    supabase.table('article') \
        .update({
            'is_featured': True,
            'featured_since': 'now()'
        }) \
        .eq('id', article_id) \
        .execute()
    
    return redirect(url_for('home'))

@main_bp.route('/admin/manage-access', methods=['GET', 'POST'])
@login_required
def manage_access():
    if not current_user.is_admin:
        abort(403)
    
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        new_role = request.form.get(f'role_{user_id}')
        success = update_user_role(user_id, new_role)
        
        if success:
            flash('Role updated successfully', 'success')
        else:
            flash('Update failed', 'error')
    
    users = User.query.all()
    return render_template('manage_access.html', users=users)

@main_bp.route('/articles')
def get_articles():
    articles = supabase.table('articles').select('*').execute()
    return render_template('articles.html', articles=articles.data)

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('user/profile.html')

def validate_password(password):
    return re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', password)

if __name__ == '__main__':
    app.run(debug=True)
import os
import click
from flask import current_app
from app import create_app, db
from app.config import Config
from app.services.ai import check_models
from app.services.news_gathering_agent import NewsFetcher

# Initialize app using factory pattern
app = create_app()

@app.cli.command()
def check_db():
    """Test database connection"""
    try:
        import psycopg2
        conn = psycopg2.connect(Config.SUPABASE_URL)
        conn.close()
        click.echo("✅ Database connection successful!")
    except Exception as e:
        click.echo(f"❌ Connection failed: {str(e)}")

@app.cli.command()
@click.option('--confirm', is_flag=True, prompt='Are you sure? This will delete all data!')
def reset_db(confirm):
    """DANGER: Full database reset"""
    if confirm:
        db.drop_all()
        db.create_all()
        click.echo("🔄 Database reset complete")

@app.cli.command()
@click.argument('email')
@click.password_option()
def create_admin(email, password):
    """Create admin user"""
    from app.services.auth import create_admin_user
    try:
        create_admin_user(email, password)
        click.echo(f"👑 Admin {email} created")
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}")

@app.cli.command()
@click.option('--hours', default=24, help='Articles older than X hours')
def cleanup_articles(hours):
    """Remove old articles"""
    from app.models import Article
    deleted = Article.delete_older_than(hours)
    click.echo(f"🗑️ Removed {deleted} articles older than {hours} hours")

@app.cli.command()
def refresh_models():
    """Update AI models from remote"""
    from app.services.ai import download_latest_models
    try:
        download_latest_models()
        click.echo("🤖 AI models updated successfully")
    except Exception as e:
        click.echo(f"❌ Model update failed: {str(e)}")

@app.cli.command()
@click.option('--source', help='Specific news source to fetch')
def fetch_news(source=None):
    """Trigger news fetching pipeline"""
    results = NewsFetcher().fetch_all(source=source)
    click.echo(f"📰 Fetched {results['new']} new articles ({results['total']} total)")

@app.cli.command()
def healthcheck():
    """System health diagnostics"""
    from app.services import database_health, cache_health
    click.echo("🏥 System Health Report")
    click.echo(f"Database: {'✅ OK' if database_health() else '❌ Down'}")
    click.echo(f"Cache: {'✅ OK' if cache_health() else '❌ Down'}")
    click.echo(f"AI Models: {'✅ Loaded' if check_models() else '❌ Missing'}")

if __name__ == '__main__':
    app.run(debug=Config.DEBUG)

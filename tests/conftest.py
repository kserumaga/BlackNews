import pytest
from app import create_app
from app.services.supabase import supabase

@pytest.fixture(scope='module')
def test_client():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SERVER_NAME": "localhost"
    })
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture(autouse=True)
def cleanup_users():
    """Cleanup test users after each test"""
    yield
    try:
        # Delete by email pattern
        test_email = "testuser@blacknews.test"
        supabase.client.auth.admin.delete_user(test_email)
    except Exception as e:
        print(f"Cleanup error: {str(e)}")

from flask import url_for, get_flashed_messages
from app.user_model import User
from app.services.supabase import supabase
import time
import pytest
from supabase import ClientError

@pytest.mark.timeout(30)
def test_successful_login(test_client):
    test_email = f"testuser{time.time()}@blacknews.test"
    test_password = "SecurePass123!"
    
    try:
        # Create user
        supabase.client.auth.admin.create_user({
            "email": test_email,
            "password": test_password,
            "email_confirm": True
        })
        
        # Test login
        response = test_client.post(
            url_for('main.login'),
            data={'email': test_email, 'password': test_password},
            follow_redirects=True
        )
        
        assert response.status_code == 200
        assert b"Recent Articles" in response.data  # Home page content
        
    except ClientError as e:
        pytest.fail(f"Supabase error: {str(e)}")
    finally:
        supabase.client.auth.admin.delete_user(test_email)

@pytest.mark.timeout(30)
def test_invalid_password(test_client):
    test_email = f"testuser{time.time()}@blacknews.test"
    valid_password = "ValidPass123!"
    
    try:
        # Create valid user
        supabase.client.auth.admin.create_user({
            "email": test_email,
            "password": valid_password,
            "email_confirm": True
        })
        
        # Attempt login with wrong password
        response = test_client.post(
            url_for('main.login'),
            data={'email': test_email, 'password': 'WrongPass123'},
            follow_redirects=True
        )
        
        assert response.status_code == 200
        assert b"Invalid email or password" in response.data
        assert b"login.html" in response.data
        
    except ClientError as e:
        pytest.fail(f"Supabase error: {str(e)}")
    finally:
        supabase.client.auth.admin.delete_user(test_email)

def test_database_connection_failure(monkeypatch, test_client):
    # Simulate database failure
    original_auth = supabase.client.auth.sign_in_with_password
    
    def mock_auth_failure(*args, **kwargs):
        raise ConnectionError("Database connection failed")
    
    monkeypatch.setattr(supabase.client.auth, "sign_in_with_password", mock_auth_failure)
    
    response = test_client.post(url_for('main.login'), data={
        'email': 'any@user.com',
        'password': 'anypass'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Login failed" in response.data

def test_empty_password(test_client):
    response = test_client.post(
        url_for('main.login'),
        data={'email': 'any@user.com', 'password': ''},
        follow_redirects=True
    )
    assert b"Please fill in both email and password" in response.data

def teardown_function():
    """Optional global teardown if needed"""
    pass

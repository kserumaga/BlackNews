from unittest.mock import patch, MagicMock
from app.user_model import User
from app.services.supabase import supabase

@patch('app.services.supabase.supabase.client.auth.sign_in_with_password')
def test_user_authentication_success(mock_auth):
    mock_auth.return_value = MagicMock(
        session=True,
        user=MagicMock(
            id='user123',
            email='test@user.com',
            created_at='2024-01-01T00:00:00',
            user_metadata={'is_admin': False}
        )
    )
    
    user = User.authenticate('test@user.com', 'validpass')
    assert user is not None
    assert user.email == 'test@user.com'
    assert user.is_admin is False

def test_authentication_invalid_credentials():
    # Create mock supabase client
    mock_supabase = MagicMock()
    mock_supabase.client.auth.sign_in_with_password.side_effect = Exception("Invalid")
    
    # Patch the supabase import in user_model
    with patch('app.user_model.supabase', mock_supabase):
        user = User.authenticate('bad@user.com', 'wrongpass')
        assert user is None

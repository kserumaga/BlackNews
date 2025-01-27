from app.user_model import User
from supabase import create_client
from flask import current_app

def update_user_role(user_id, new_role):
    """Update user role in Supabase"""
    supabase = create_client(
        current_app.config['SUPABASE_URL'],
        current_app.config['SUPABASE_KEY']
    )
    
    try:
        # Update raw_user_meta_data field
        response = supabase.table('users', schema='auth').update({
            'raw_user_meta_data': {'is_admin': new_role == 'admin'}
        }).eq('id', user_id).execute()
        
        return True if response.data else False
    except Exception as e:
        current_app.logger.error(f"Role update error: {str(e)}")
        return False

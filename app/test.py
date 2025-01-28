import sys
sys.path.append('C:/Users/Kizito/Documents/GitHub/BlackNews')  # Add project root to path

from app import create_app
from app.services.supabase import supabase

app = create_app()

with app.app_context():
    try:
        response = supabase.client.auth.sign_up({
            "email": "kserumaga@gmail.com",
            "password": "test1234"
        })
        
        if response.user:
            print(f"User created: {response.user.email}")
            print("User ID:", response.user.id)
        else:
            print("Error creating user:", response)
            
    except Exception as e:
        print("Signup error:", str(e))

print("\nTesting login...")
try:
    login_response = supabase.client.auth.sign_in_with_password({
        "email": "kserumaga@gmail.com",
        "password": "test1234"
    })
    
    if login_response.user:
        print("Login successful!")
        print("Session:", login_response.session)
    else:
        print("Login failed:", login_response)
        
except Exception as e:
    print("Login error:", str(e))
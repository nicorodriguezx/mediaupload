import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def load_credentials():
    """Load and validate API credentials from environment variables."""
    access_token = os.getenv("ACCESS_TOKEN")
    ig_user_id = os.getenv("IG_USER_ID")
    
    if not access_token:
        raise ValueError("ACCESS_TOKEN is not set in the environment variables.")
    if not ig_user_id:
        raise ValueError("IG_USER_ID is not set in the environment variables.")
        
    return access_token, ig_user_id

def fetch_user_info(access_token):
    """Fetch user information from Instagram Graph API."""
    url = f"https://graph.instagram.com/v21.0/me"
    params = {
        "fields": "id,user_id,username,name,account_type,profile_picture_url,followers_count,follows_count,media_count",
        "access_token": access_token
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Request Error:", str(e))
        return None
    except Exception as e:
        print("Error:", str(e))
        return None

def fetch_user_media(access_token, ig_user_id):
    """Fetch user media objects from Instagram Graph API."""
    url = f"https://graph.instagram.com/v21.0/{ig_user_id}/media"
    params = {
        "access_token": access_token
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Request Error:", str(e))
        return None
    except Exception as e:
        print("Error:", str(e))
        return None

def main():
    try:
        # Load credentials
        access_token, ig_user_id = load_credentials()
        
        # Fetch user information
        user_info = fetch_user_info(access_token)
        if user_info:
            print("User Information:", user_info)
        
        # Fetch media objects
        media_info = fetch_user_media(access_token, ig_user_id)
        if media_info:
            print("Media Objects:", media_info)
            
    except ValueError as e:
        print("Configuration Error:", str(e))

if __name__ == "__main__":
    main() 
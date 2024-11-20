import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_instagram_upload():
    # API endpoint (assuming Flask is running locally on default port)
    url = "http://localhost:5000/upload_instagram"
    
    # Prepare the payload using environment variables for sensitive data
    payload = {
        "user_id": os.getenv("IG_USER_ID"),
        "access_token": os.getenv("ACCESS_TOKEN"),
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/6/62/NCI_Visuals_Food_Hamburger.jpg",
        "caption": """Delicious hamburger! 🍔

#foodie #hamburger #delicious #instafood #foodphotography"""
    }

    # Send POST request
    response = requests.post(url, json=payload)
    
    # Print results
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    test_instagram_upload() 
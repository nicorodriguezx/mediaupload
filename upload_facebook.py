import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

def upload_facebook_post(user_id, access_token, image_url, message):
    """Upload an image to Facebook
    
    Args:
        user_id (str): Facebook User ID
        access_token (str): Facebook Access Token
        image_url (str): URL of the image to post
        message (str): Message for the post
    """
    url = f"https://graph.facebook.com/v21.0/{user_id}/photos"
    
    payload = {
        "url": image_url,
        "caption": message,
        "access_token": access_token
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        print("Facebook Post Created:", result)
        return result.get("id")
    except requests.exceptions.RequestException as e:
        print("Error uploading to Facebook:", str(e))
        return None

@app.route('/upload_facebook', methods=['POST'])
def upload_facebook_post_endpoint():
    """Flask endpoint to handle Facebook post uploads"""
    try:
        data = request.get_json()
        
        # Extract required fields from request
        user_id = data.get('user_id')
        access_token = data.get('access_token')
        image_url = data.get('image_url')
        message = data.get('message')
        
        # Validate required fields
        if not all([user_id, access_token, image_url, message]):
            return jsonify({
                'error': 'Missing required fields. Please provide user_id, access_token, image_url, and message'
            }), 400

        # Upload the post to Facebook
        media_id = upload_facebook_post(
            user_id=user_id,
            access_token=access_token,
            image_url=image_url,
            message=message
        )
        
        if not media_id:
            return jsonify({'error': 'Failed to upload media to Facebook'}), 500

        return jsonify({
            'success': True,
            'media_id': media_id
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
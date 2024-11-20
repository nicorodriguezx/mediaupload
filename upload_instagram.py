import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

def create_media_container(user_id, access_token, image_url, caption, media_type):
    """Create a media container for the image with caption and media type
    
    Args:
        user_id (str): Instagram User ID
        access_token (str): Instagram Access Token
        image_url (str): URL of the image to post
        caption (str): Caption for the media
        media_type (str): Type of media ('FEED', 'STORIES', 'IMAGE', etc.)
    """
    url = f"https://graph.instagram.com/v21.0/{user_id}/media"
    
    payload = {
        "image_url": image_url,
        "caption": caption,
        "media_type": media_type,
        "access_token": access_token
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        print("Media Container Created:", result)
        return result.get("id")
    except requests.exceptions.RequestException as e:
        print("Error creating media container:", str(e))
        return None

def publish_media(user_id, access_token, container_id):
    """Publish the media using the container ID
    
    Args:
        user_id (str): Instagram User ID
        access_token (str): Instagram Access Token
        container_id (str): Container ID from create_media_container
    """
    url = f"https://graph.instagram.com/v21.0/{user_id}/media_publish"
    
    payload = {
        "creation_id": container_id,
        "access_token": access_token
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        print("Media Published:", result)
        return result.get("id")
    except requests.exceptions.RequestException as e:
        print("Error publishing media:", str(e))
        return None

@app.route('/upload_instagram', methods=['POST'])
def upload_instagram_post():
    """Flask endpoint to handle Instagram post uploads"""
    try:
        data = request.get_json()
        
        # Extract required fields from request
        user_id = data.get('user_id')
        access_token = data.get('access_token')
        image_url = data.get('image_url')
        caption = data.get('caption')
        
        # Validate required fields
        if not all([user_id, access_token, image_url, caption]):
            return jsonify({
                'error': 'Missing required fields. Please provide user_id, access_token, image_url, and caption'
            }), 400

        # Create and publish the post
        container_id = create_media_container(
            user_id=user_id,
            access_token=access_token,
            image_url=image_url,
            caption=caption,
            media_type="IMAGE"
        )
        
        if not container_id:
            return jsonify({'error': 'Failed to create media container'}), 500

        media_id = publish_media(user_id, access_token, container_id)
        
        if not media_id:
            return jsonify({'error': 'Failed to publish media'}), 500

        return jsonify({
            'success': True,
            'media_id': media_id
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
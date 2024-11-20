import os
from flask import Flask, redirect, url_for, session, request, render_template
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  # Set a secret key for session management

# Facebook App credentials
FB_APP_ID = os.getenv("FB_APP_ID")
FB_APP_SECRET = os.getenv("FB_APP_SECRET")
FB_REDIRECT_URI = os.getenv("FB_REDIRECT_URI")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    # Redirect to Facebook for login
    return redirect(f"https://www.facebook.com/v21.0/dialog/oauth?client_id={FB_APP_ID}&redirect_uri={FB_REDIRECT_URI}&scope=email,public_profile")

@app.route('/callback')
def callback():
    # Get the authorization code from the URL
    code = request.args.get('code')
    
    # Exchange the code for an access token
    token_url = f"https://graph.facebook.com/v21.0/oauth/access_token?client_id={FB_APP_ID}&redirect_uri={FB_REDIRECT_URI}&client_secret={FB_APP_SECRET}&code={code}"
    response = requests.get(token_url)
    data = response.json()
    
    # Get the access token
    access_token = data.get('access_token')
    
    # Use the access token to get user information
    user_info_url = f"https://graph.facebook.com/me?fields=id,name,email&access_token={access_token}"
    user_info_response = requests.get(user_info_url)
    user_info = user_info_response.json()
    
    # Store user info in session
    session['user'] = user_info
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    user = session.get('user')
    if user:
        return render_template('profile.html', user=user)
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
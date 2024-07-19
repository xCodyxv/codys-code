# This is made to work in google colab

# pip install
!pip install Flask pyngrok

# Set your ngrok authtoken (replace 'YOUR_NGROK_AUTH_TOKEN' with your actual token)
!ngrok authtoken YOUR_NGROK_AUTH_TOKEN

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Bare Bones Script | you can change this whole code to better suit the task at hand as this just shows how to do a website front end and how I use and set up the gemini 1.5 flash model in my projects

from flask import Flask, request, jsonify, render_template_string
from google.generativeai import GenerativeModel
import google.generativeai as genai
from google.colab import userdata
import os
from pyngrok import ngrok

# Setup your API key using the Colab userdata module
GOOGLE_API_KEY = userdata.get('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("API key not found. Please set your API key in Colab.")

# Initialize the Gemini 1.5 model
model = GenerativeModel('gemini-1.5-flash')

# Create Flask app
app = Flask(__name__)

# Define a route for the homepage
@app.route('/')
def ai_assistant():
    return render_template_string(html_content)

# Define a route for handling chat messages
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'response': 'Error: No message received.'})

    # Generate the response from the Gemini 1.5 model
    response = model.generate_content(user_message)
    return jsonify({'response': response.text})

# HTML content
html_content = '''

'''

# Run the Flask app with ngrok
if __name__ == '__main__':
    # Start ngrok to tunnel the local Flask app to a public URL
    public_url = ngrok.connect(5000)
    print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:5000\"".format(public_url))

    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)

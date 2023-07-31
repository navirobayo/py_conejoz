import os
import requests
from flask import Flask, Blueprint, request, jsonify, send_from_directory
from gradio_client import Client
from urllib.parse import urlparse
import time

app = Flask(__name__)
main = Blueprint('main', __name__)

# Directory to store the images
IMAGE_DIR = os.path.join(app.root_path, "images")
os.makedirs(IMAGE_DIR, exist_ok=True)

@main.route('/')
def index():
    return 'Hello Conejoz, here you will be able to communicate with the API and the Flutter app'

# New route to handle API requests
@main.route('/process_text', methods=['POST'])
def process_text():
    try:
        input_text = request.form.get('text')  # Get the text input from the request

        # Make the API request to the ImageCreator API using gradio_client
        client = Client("https://navirobayo-conejoz.hf.space/")
        result = client.predict(input_text, api_name="/predict")
        image_url = result.strip()  # Assuming the result is the image URL as a string

        # Extract the filename from the URL
        image_filename = os.path.basename(urlparse(image_url).path)

        # Generate a unique filename based on the current timestamp
        unique_filename = f"{int(time.time())}.jpg"

        # Download the image from the URL using requests
        response = requests.get(image_url)
        response.raise_for_status()  # Check for any download errors

        # Save the image with the unique filename
        image_path = os.path.join(IMAGE_DIR, unique_filename)
        with open(image_path, 'wb') as f:
            f.write(response.content)

        return jsonify({'image_url': f'/get_image/{unique_filename}'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to serve the image
@main.route('/get_image/<filename>')
def get_image(filename):
    image_path = os.path.join(IMAGE_DIR, filename)
    return send_from_directory(IMAGE_DIR, filename)

if __name__ == '__main__':
    # Register the blueprint and run the app
    app.register_blueprint(main)

    # For local development, use host='localhost'
    # For public access, use host='0.0.0.0'
    app.run(host='0.0.0.0', port=8080)

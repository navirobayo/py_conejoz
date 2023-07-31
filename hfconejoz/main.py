import os
import requests
from flask import Flask, Blueprint, request, jsonify, send_file
from gradio_client import Client
import tempfile
import shutil

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
        
        # Assuming the result is the image file path as a string
        local_image_path = result.strip()  

        # Copy the image file to the server's images directory
        _, image_filename = os.path.split(local_image_path)
        server_image_path = os.path.join(IMAGE_DIR, image_filename)
        shutil.copyfile(local_image_path, server_image_path)

        # Return the URL to access the image
        image_url = f"/get_image/{image_filename}"

        return jsonify({'image_url': image_url})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to serve the image
@main.route('/get_image/<filename>')
def get_image(filename):
    return send_file(os.path.join(IMAGE_DIR, filename))

if __name__ == '__main__':
    # Register the blueprint and run the app
    app.register_blueprint(main)

    # For local development, use host='localhost'
    # For public access, use host='0.0.0.0'
    app.run(host='0.0.0.0', port=8080)

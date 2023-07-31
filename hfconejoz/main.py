from flask import Blueprint, request, jsonify
from gradio_client import Client

main = Blueprint('main', __name__)

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

        if image_url:
            return jsonify({'image_url': image_url})

        return jsonify({'error': 'Image creation failed'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

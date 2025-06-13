from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Set your OpenAI key from environment or directly
client = OpenAI(api_key = "OPEN_AI_APIKEY")

@app.route('/ping')
def ping():
    return jsonify({"status": "alive"})

@app.route('/summarize', methods=['GET', 'POST', 'OPTIONS'])
def handle_summarize():
    if request.method == 'OPTIONS':
        # CORS preflight request handling
        return '', 204

    if request.method == 'GET':
        return jsonify({"status": "Backend is ready"})

    if request.method == 'POST':
        # Check if Content-Type is application/json
        if request.content_type != 'application/json':
            return jsonify({'error': "Unsupported Media Type. Please set Content-Type to 'application/json'"}), 415

        try:
            data = request.get_json(force=True)  # ensures JSON parsing
        except Exception:
            return jsonify({'error': "Invalid JSON data"}), 400

        if not data or 'text' not in data:
            return jsonify({'error': 'Missing "text" in request'}), 400

        text = str(data.get('text'))[:15000]

        try:
            # Call OpenAI API for summarization
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                    {"role": "user", "content": f"Please summarize the following text in 3-5 concise bullet points:\n\n{text}"}
                ],
                temperature=0.5,
                max_tokens=500
            )

            summary = response.choices[0].message.content
            return jsonify({'summary': summary})

        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)



from flask import Flask, request, jsonify
import fitz
import os

app = Flask(__name__)

@app.route('/extraer_texto', methods=['POST'])
def extract_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        first_page = doc.load_page(0)
        text = first_page.get_text()
        return jsonify({'text': text}), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/', methods=['GET'])
def home():
    return "PDF Text Extractor API - Flask is running.", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
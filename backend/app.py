from flask import Flask, request, jsonify
from flask_cors import CORS
from model import predict_news
import nltk

# Download required NLTK data
nltk.download('stopwords')
nltk.download('punkt')

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin requests

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Get prediction
        result = predict_news(text)
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'Server is running'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
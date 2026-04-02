import re
import string
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob
import nltk

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Text preprocessing
def preprocess_text(text):
    """Clean and preprocess text for model input"""
    if pd.isna(text):
        return ""
    
    # Lowercase
    text = str(text).lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Tokenize and remove stopwords
    try:
        tokens = word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word not in stop_words and len(word) > 2]
        return ' '.join(tokens)
    except:
        return text

# Load model
try:
    model = joblib.load('../models/fake_news_model.pkl')
    vectorizer = joblib.load('../models/tfidf_vectorizer.pkl')
    MODEL_LOADED = True
    print("✅ Model loaded successfully!")
except Exception as e:
    MODEL_LOADED = False
    print(f"⚠️ Model not found: {e}")

def analyze_sentiment(text):
    """Analyze sentiment of the text"""
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            return "Positive", polarity
        elif polarity < -0.1:
            return "Negative", polarity
        else:
            return "Neutral", polarity
    except:
        return "Unknown", 0

def extract_features(text):
    """Extract additional features from text"""
    features = {}
    
    # Text length
    features['text_length'] = len(text)
    features['word_count'] = len(text.split())
    
    # Count exclamation and question marks (sensational indicators)
    features['exclamation_count'] = text.count('!')
    features['question_count'] = text.count('?')
    
    # All caps words (shouting - often in fake news)
    words = text.split()
    features['caps_ratio'] = sum(1 for w in words if w.isupper()) / len(words) if words else 0
    
    return features

def predict_news(text):
    """Main prediction function with enhanced analysis"""
    if not MODEL_LOADED:
        return {
            'prediction': 'Unknown',
            'confidence': 0,
            'message': 'Model not trained yet. Run train_model.py first!'
        }
    
    # Preprocess
    cleaned_text = preprocess_text(text)
    
    if not cleaned_text or len(cleaned_text.split()) < 5:
        return {
            'prediction': 'Unknown',
            'confidence': 0,
            'message': 'Text too short for accurate prediction'
        }
    
    # Vectorize
    text_vectorized = vectorizer.transform([cleaned_text])
    
    # Predict
    prediction = model.predict(text_vectorized)[0]
    probabilities = model.predict_proba(text_vectorized)[0]
    confidence = max(probabilities) * 100
    
    # Get sentiment
    sentiment, polarity = analyze_sentiment(text)
    
    # Extract features
    extra_features = extract_features(text)
    
    # Determine label
    label = "Real News" if prediction == 1 else "Fake News"
    status = "real" if prediction == 1 else "fake"
    
    # Generate explanation
    explanation = []
    
    if extra_features['exclamation_count'] > 3:
        explanation.append("High use of exclamation marks (sensational)")
    
    if extra_features['caps_ratio'] > 0.3:
        explanation.append("Excessive use of capital letters")
    
    if abs(polarity) > 0.5:
        explanation.append(f"Strong {sentiment.lower()} sentiment detected")
    
    if confidence < 70:
        explanation.append("Low confidence - manual verification recommended")
    
    return {
        'prediction': label,
        'status': status,
        'confidence': round(confidence, 2),
        'sentiment': sentiment,
        'sentiment_score': round(polarity, 2),
        'word_count': extra_features['word_count'],
        'explanation': explanation if explanation else ["Analysis complete"],
        'preview': cleaned_text[:150] + "..."
    }
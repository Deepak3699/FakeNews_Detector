# 📰 Fake News Detector - AI Powered

An intelligent web application that uses Machine Learning and Natural Language Processing to detect fake news articles with high accuracy.

---

## 🎯 Features

- ✅ **AI-Powered Detection** - 98%+ accuracy using Logistic Regression
- ✅ **Sentiment Analysis** - Analyzes emotional tone of articles
- ✅ **Confidence Scoring** - Shows prediction confidence percentage
- ✅ **Detailed Insights** - Explains why content is classified as fake/real
- ✅ **History Tracking** - Saves last 5 analyzed articles
- ✅ **Responsive Design** - Works on desktop, tablet, and mobile
- ✅ **Real-time Analysis** - Fast predictions in seconds

---

## 🛠️ Tech Stack

### **Backend**
- Python 3.8+
- Flask (Web Framework)
- Scikit-learn (Machine Learning)
- NLTK (Natural Language Processing)
- Pandas & NumPy (Data Processing)

### **Frontend**
- HTML5
- CSS3 (Custom Styling)
- Vanilla JavaScript
- Font Awesome (Icons)

### **Machine Learning**
- **Algorithm**: Logistic Regression
- **Vectorization**: TF-IDF
- **Dataset**: 44,000+ news articles (Fake & Real)

---

## 📁 Project Structure

```
fake-news-detector/
│
├── backend/
│   ├── app.py                 # Flask API server
│   ├── model.py               # ML model & prediction logic
│   ├── train_model.py         # Model training script
│   ├── test_api.py            # Testing script
│   └── requirements.txt       # Python dependencies
│
├── frontend/
│   ├── index.html             # Main HTML page
│   ├── css/
│   │   └── style.css          # Styling
│   └── js/
│       └── app.js             # Frontend logic
│
├── models/
│   ├── fake_news_model.pkl    # Trained ML model
│   ├── tfidf_vectorizer.pkl   # Text vectorizer
│   └── model_metadata.pkl     # Model information
│
├── data/
│   └── News_dataset/
│       ├── Fake.csv           # Fake news dataset
│       └── True.csv           # Real news dataset
│
└── README.md                  # This file
```

---

## 🚀 Installation & Setup

### **Prerequisites**
- Python 3.8 or higher
- pip (Python package manager)
- Web browser (Chrome, Firefox, Edge, etc.)

### **Step 1: Clone/Download the Project**

```bash
# Clone repository (if using Git)
git clone <your-repo-url>
cd fake-news-detector

# OR simply download and extract the ZIP file
```

---

### **Step 2: Setup Backend**

```bash
# Navigate to backend folder
cd backend

# Install required Python packages
pip install -r requirements.txt

# This will install:
# - flask
# - flask-cors
# - pandas
# - numpy
# - scikit-learn
# - nltk
# - joblib
# - textblob
```

---

### **Step 3: Train the Model**

```bash
# Make sure you're in the backend folder
python train_model.py
```

**Expected Output:**
```
🔄 Loading datasets...
✅ Fake news articles: 23502
✅ Real news articles: 21417

📊 Total articles: 44919
🧹 Preprocessing text...
✅ Preprocessing complete!

🤖 Training model...
✅ Model trained!

🎯 Accuracy: 98.81%

✅ Model and vectorizer saved successfully!
```

⏱️ **Training Time**: 2-5 minutes (depending on your system)

---

### **Step 4: Start Backend Server**

```bash
# Make sure you're in the backend folder
python app.py
```

**Expected Output:**
```
✅ Model loaded successfully!
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

🟢 **Keep this terminal window open!**

---

### **Step 5: Open Frontend**

**Option 1: Direct File Opening**
```bash
# Navigate to frontend folder
cd ../frontend

# Open index.html in your browser
# Windows:
start index.html

# Mac:
open index.html

# Linux:
xdg-open index.html
```

**Option 2: Using Python HTTP Server** (Recommended)
```bash
# In the frontend folder
python -m http.server 8000

# Then open browser and go to:
# http://localhost:8000
```

**Option 3: VS Code Live Server**
- Install "Live Server" extension in VS Code
- Right-click `index.html` → "Open with Live Server"

---

## 💡 How to Use

### **1. Enter News Text**
- Paste any news article, headline, or text (minimum 10 words)
- The word counter updates in real-time

### **2. Click "Analyze News"**
- The app sends text to the backend API
- AI model processes and analyzes the content
- Results appear in 2-3 seconds

### **3. View Results**
The app shows:
- ✅ **Prediction**: Real News or ❌ Fake News
- 📊 **Confidence Score**: Percentage (0-100%)
- 😊 **Sentiment**: Positive/Negative/Neutral
- 🔍 **Insights**: Why it's classified as fake/real
- 📄 **Preview**: Processed text

### **4. Check History**
- Last 5 analyzed articles are saved
- Stored in browser's local storage
- Persists even after page refresh

---

## 🧪 Testing the App

### **Test with Sample Fake News:**
```
BREAKING NEWS! Scientists SHOCKED by this ONE weird trick! 
Doctors HATE him! Government wants to BAN this miracle cure!
Click NOW before it's too late!!!
```

**Expected Result**: ❌ Fake News (High confidence)

---

### **Test with Sample Real News:**
```
The Federal Reserve announced today that interest rates will 
remain unchanged following their monthly policy meeting. 
Economic analysts suggest this decision reflects ongoing 
concerns about inflation and employment rates.
```

**Expected Result**: ✅ Real News (High confidence)

---

## 📊 How It Works

### **Backend Process:**

```
1. User submits text
         ↓
2. Text preprocessing (cleaning, tokenization)
         ↓
3. Remove stopwords, URLs, punctuation
         ↓
4. TF-IDF Vectorization (convert text to numbers)
         ↓
5. Logistic Regression Model prediction
         ↓
6. Sentiment Analysis (TextBlob)
         ↓
7. Generate confidence score & insights
         ↓
8. Send JSON response to frontend
```

### **Machine Learning Model:**

- **Algorithm**: Logistic Regression
- **Training Data**: 44,919 articles
- **Features**: 10,000 TF-IDF features
- **Accuracy**: 98.81%
- **Precision**: 99% (Fake), 98% (Real)
- **Recall**: 98% (Fake), 99% (Real)

---

## 🔧 Troubleshooting

### **Issue: "Model not found" error**
**Solution:**
```bash
cd backend
python train_model.py
```

---

### **Issue: "Cannot connect to backend"**
**Solution:**
1. Check if backend is running on `http://localhost:5000`
2. Check console for CORS errors
3. Restart backend: `python app.py`

---

### **Issue: "Prediction accuracy is low"**
**Solution:**
- Make sure text has at least 10 words
- Use complete sentences, not single words
- Retrain model if needed

---

### **Issue: Port 5000 already in use**
**Solution:**
```python
# In app.py, change the port:
app.run(debug=True, port=5001)

# Then update API_URL in frontend/js/app.js:
const API_URL = 'http://localhost:5001/api/predict';
```

---

## 📝 API Documentation

### **Endpoint: `/api/predict`**

**Method:** POST

**Request Body:**
```json
{
  "text": "Your news article text here..."
}
```

**Response:**
```json
{
  "prediction": "Real News",
  "status": "real",
  "confidence": 97.45,
  "sentiment": "Neutral",
  "sentiment_score": 0.05,
  "word_count": 45,
  "explanation": [
    "Analysis complete"
  ],
  "preview": "federal reserve announced interest rates..."
}
```

---

### **Endpoint: `/api/health`**

**Method:** GET

**Response:**
```json
{
  "status": "Server is running"
}
```

---

## 🎓 For Professors/Evaluators

### **Key Highlights:**

1. **High Accuracy**: 98.81% on test data
2. **Explainable AI**: Shows why predictions are made
3. **Real-world Dataset**: 44,000+ actual news articles
4. **Complete Pipeline**: Data preprocessing → Training → Deployment
5. **Production Ready**: Error handling, validation, CORS support
6. **User Experience**: Responsive design, loading states, history

### **Advanced Features:**
- TF-IDF with bigrams (1-2 word combinations)
- Sentiment polarity analysis
- Feature extraction (caps ratio, punctuation analysis)
- Client-side validation
- Local storage persistence

---

## 📚 Dataset Information

**Source Files:**
- `Fake.csv`: 23,502 fake news articles
- `True.csv`: 21,417 real news articles

**Columns:**
- `title`: Article headline
- `text`: Full article content
- `subject`: News category
- `date`: Publication date

**Preprocessing:**
- Combined title + text for better context
- Removed stopwords, URLs, punctuation
- Tokenization and lemmatization
- TF-IDF vectorization (10,000 features)

---

## 🔮 Future Enhancements

- [ ] URL scraping - Analyze news from any website
- [ ] Multi-language support
- [ ] Source credibility checker
- [ ] Fact-check API integration
- [ ] Browser extension
- [ ] Export reports as PDF
- [ ] Deep learning models (BERT, GPT)
- [ ] Real-time news monitoring
- [ ] User authentication
- [ ] Batch processing

---

## 📄 License

This project is created for educational purposes.

---

## 👨‍💻 Author

** Deepak **  
**Btech Cse **: 5th Semester Project  
**Year**: 2026

---

## 🙏 Acknowledgments

- Dataset: Kaggle Fake News Dataset
- Libraries: Scikit-learn, NLTK, Flask
- Icons: Font Awesome

---

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review console logs for errors
3. Ensure both backend and frontend are running
4. Verify dataset files are in correct location

---

## ✅ Quick Start Checklist

- [ ] Python 3.8+ installed
- [ ] Install requirements: `pip install -r requirements.txt`
- [ ] Train model: `python train_model.py`
- [ ] Start backend: `python app.py`
- [ ] Open `index.html` in browser
- [ ] Test with sample text
- [ ] Check results and history

---

**🎉 Congratulations! Your Fake News Detector is ready to use!**


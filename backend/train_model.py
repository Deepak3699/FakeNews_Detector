import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
from model import preprocess_text
import os

print("🔄 Loading datasets...")

# Load datasets
fake_df = pd.read_csv('../data/News_dataset/Fake.csv', low_memory=False)
true_df = pd.read_csv('../data/News_dataset/True.csv', low_memory=False)

# Add labels
fake_df['label'] = 0  # Fake news
true_df['label'] = 1  # Real news

print(f"✅ Fake news articles: {len(fake_df)}")
print(f"✅ Real news articles: {len(true_df)}")

# Combine datasets
df = pd.concat([fake_df, true_df], ignore_index=True)

# Combine title and text for better analysis
df['content'] = df['title'] + ' ' + df['text']

# Remove null values
df = df.dropna(subset=['content'])

print(f"\n📊 Total articles: {len(df)}")
print(f"📊 Dataset balance:\n{df['label'].value_counts()}")

# Shuffle dataset
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

print("\n🧹 Preprocessing text...")

# Preprocess text
df['cleaned_content'] = df['content'].apply(preprocess_text)

# Remove empty cleaned content
df = df[df['cleaned_content'].str.strip() != '']

print("✅ Preprocessing complete!")

# Split data (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(
    df['cleaned_content'], 
    df['label'], 
    test_size=0.2, 
    random_state=42,
    stratify=df['label']  # Maintain label balance
)

print(f"\n📈 Training set: {len(X_train)}")
print(f"📈 Testing set: {len(X_test)}")

# TF-IDF Vectorization
print("\n🔢 Creating TF-IDF vectors...")
vectorizer = TfidfVectorizer(
    max_features=10000,     # Top 10k important words
    ngram_range=(1, 2),     # Unigrams and bigrams
    min_df=5,               # Ignore rare words
    max_df=0.8              # Ignore too common words
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

print("✅ Vectorization complete!")

# Train Logistic Regression model (better than Naive Bayes)
print("\n🤖 Training model...")
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_vec, y_train)

print("✅ Model trained!")

# Evaluate
print("\n📊 Evaluating model...")
y_pred = model.predict(X_test_vec)

accuracy = accuracy_score(y_test, y_pred)
print(f"\n🎯 Accuracy: {accuracy * 100:.2f}%")

print("\n📋 Classification Report:")
print(classification_report(y_test, y_pred, target_names=['Fake News', 'Real News']))

print("\n🔢 Confusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(cm)

# Create models directory if not exists
os.makedirs('../models', exist_ok=True)

# Save model and vectorizer
joblib.dump(model, '../models/fake_news_model.pkl')
joblib.dump(vectorizer, '../models/tfidf_vectorizer.pkl')

print("\n✅ Model and vectorizer saved successfully!")
print("📁 Location: ../models/")

# Save some metadata
metadata = {
    'accuracy': accuracy,
    'total_samples': len(df),
    'features': vectorizer.get_feature_names_out()[:100].tolist(),
    'model_type': 'Logistic Regression'
}

joblib.dump(metadata, '../models/model_metadata.pkl')
print("✅ Model metadata saved!")
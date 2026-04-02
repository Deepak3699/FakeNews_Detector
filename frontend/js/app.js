// ========================================
// CONFIGURATION
// ========================================
const API_URL = 'http://localhost:5000/api/predict';
const MIN_WORDS = 10;
const MAX_HISTORY = 5;

// ========================================
// DOM ELEMENTS
// ========================================
const newsText = document.getElementById('newsText');
const wordCount = document.getElementById('wordCount');
const charCount = document.getElementById('charCount');
const analyzeBtn = document.getElementById('analyzeBtn');
const clearBtn = document.getElementById('clearBtn');
const errorMessage = document.getElementById('errorMessage');
const resultSection = document.getElementById('resultSection');
const resultCard = document.getElementById('resultCard');
const loadingOverlay = document.getElementById('loadingOverlay');
const historySection = document.getElementById('historySection');
const historyGrid = document.getElementById('historyGrid');

// ========================================
// STATE MANAGEMENT
// ========================================
let history = JSON.parse(localStorage.getItem('newsHistory')) || [];

// ========================================
// EVENT LISTENERS
// ========================================
newsText.addEventListener('input', updateCounters);
analyzeBtn.addEventListener('click', analyzeNews);
clearBtn.addEventListener('click', clearForm);

// ========================================
// FUNCTIONS
// ========================================

// Update word and character counters
function updateCounters() {
    const text = newsText.value.trim();
    const words = text.split(/\s+/).filter(word => word.length > 0);

    wordCount.textContent = words.length;
    charCount.textContent = text.length;

    // Hide error when typing
    if (errorMessage.style.display !== 'none') {
        hideError();
    }
}

// Show error message
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    errorMessage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Hide error message
function hideError() {
    errorMessage.style.display = 'none';
}

// Show loading overlay
function showLoading() {
    loadingOverlay.style.display = 'flex';
}

// Hide loading overlay
function hideLoading() {
    loadingOverlay.style.display = 'none';
}

// Validate input
function validateInput(text) {
    if (!text.trim()) {
        showError('Please enter some text to analyze');
        return false;
    }

    const words = text.split(/\s+/).filter(word => word.length > 0);
    if (words.length < MIN_WORDS) {
        showError(`Please enter at least ${MIN_WORDS} words for accurate analysis`);
        return false;
    }

    return true;
}

// Analyze news
async function analyzeNews() {
    const text = newsText.value;

    // Validate input
    if (!validateInput(text)) {
        return;
    }

    // Disable button and show loading
    analyzeBtn.disabled = true;
    showLoading();
    hideError();

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text })
        });

        if (!response.ok) {
            throw new Error('Failed to analyze. Please check if backend server is running.');
        }

        const result = await response.json();

        // Display result
        displayResult(result);

        // Add to history
        addToHistory(text, result);

        // Scroll to result
        resultSection.scrollIntoView({ behavior: 'smooth' });

    } catch (error) {
        console.error('Error:', error);
        showError('Failed to analyze. Make sure backend is running on http://localhost:5000');
    } finally {
        analyzeBtn.disabled = false;
        hideLoading();
    }
}

// Display result
function displayResult(result) {
    const isFake = result.status === 'fake';
    const iconClass = isFake ? 'fa-times-circle fake' : 'fa-check-circle real';
    const cardClass = isFake ? 'fake' : 'real';

    let explanationHTML = '';
    if (result.explanation && result.explanation.length > 0) {
        explanationHTML = `
            <div class="explanation-section">
                <h3><i class="fas fa-lightbulb"></i> Analysis Insights:</h3>
                <ul class="explanation-list">
                    ${result.explanation.map(item => `<li>${item}</li>`).join('')}
                </ul>
            </div>
        `;
    }

    const sentimentClass = result.sentiment.toLowerCase();

    resultCard.innerHTML = `
        <div class="result-header">
            <i class="fas ${iconClass} result-icon"></i>
            <h2>${result.prediction}</h2>
        </div>

        <div class="confidence-meter">
            <div class="confidence-label">
                <i class="fas fa-chart-bar"></i> Confidence Score
            </div>
            <div class="progress-bar">
                <div class="progress-fill ${result.status}" style="width: ${result.confidence}%">
                    <span class="progress-text">${result.confidence}%</span>
                </div>
            </div>
        </div>

        <div class="result-details">
            <div class="detail-item">
                <span class="detail-label">Sentiment:</span>
                <span class="detail-value sentiment-${sentimentClass}">${result.sentiment}</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">Sentiment Score:</span>
                <span class="detail-value">${result.sentiment_score}</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">Word Count:</span>
                <span class="detail-value">${result.word_count}</span>
            </div>
        </div>

        ${explanationHTML}

        <div class="preview-section">
            <h4><i class="fas fa-file-alt"></i> Processed Text Preview:</h4>
            <p class="preview-text">${result.preview}</p>
        </div>
    `;

    resultCard.className = `result-card ${cardClass}`;
    resultSection.style.display = 'block';
}

// Add to history
function addToHistory(text, result) {
    const historyItem = {
        id: Date.now(),
        text: text.substring(0, 100) + (text.length > 100 ? '...' : ''),
        result: result,
        timestamp: new Date().toLocaleString()
    };

    // Add to beginning of array
    history.unshift(historyItem);

    // Keep only last MAX_HISTORY items
    if (history.length > MAX_HISTORY) {
        history = history.slice(0, MAX_HISTORY);
    }

    // Save to localStorage
    localStorage.setItem('newsHistory', JSON.stringify(history));

    // Display history
    displayHistory();
}

// Display history
function displayHistory() {
    if (history.length === 0) {
        historySection.style.display = 'none';
        return;
    }

    historyGrid.innerHTML = history.map(item => `
        <div class="history-card">
            <div class="history-header">
                <span class="badge ${item.result.status}">${item.result.prediction}</span>
                <span class="timestamp">${item.timestamp}</span>
            </div>
            <p class="history-text">${item.text}</p>
            <div class="history-confidence">
                Confidence: ${item.result.confidence}%
            </div>
        </div>
    `).join('');

    historySection.style.display = 'block';
}

// Clear form
function clearForm() {
    newsText.value = '';
    updateCounters();
    hideError();
    resultSection.style.display = 'none';
}

// ========================================
// INITIALIZATION
// ========================================
document.addEventListener('DOMContentLoaded', () => {
    updateCounters();
    displayHistory();
});

// ========================================
// KEYBOARD SHORTCUTS
// ========================================
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to analyze
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        analyzeNews();
    }

    // Escape to clear
    if (e.key === 'Escape') {
        clearForm();
    }
});
# Government-Name-Management-Portal

The **Government Name Management Portal** is an intelligent web-based tool designed to identify, compare, and match Hindi names, even when they contain typos, transliteration variations, or phonetic differences. It uses a machine learning model trained on synthetic variations of real Hindi names to make accurate matching decisions.

---

## 🔍 Features

- 🧠 **AI-Powered Name Matching**: Uses a Random Forest model trained with rich features (Levenshtein distance, phonetic encoding, n-gram similarity, etc.).
- 🔁 **Handles Misspellings and Variations**: Robust against typos, phonetic errors, and transliteration inconsistencies common in Hindi names.
- 🌐 **REST API with Flask**: Provides endpoints to compare names, search among candidates, and retrieve feature importances.
- 📊 **Feature Importance Analysis**: Understands which features contribute most to the matching decisions.
- 🌟 **Web Interface**: Clean and simple static UI (HTML/CSS/JS) to interact with the backend.

---

## 📁 Project Structure

```plaintext
fuzzy_logic/
│
├── HindiNameMatcher.py # Model training and feature extraction
├── matcher.py # Core logic for feature extraction and matching
├── Namedatasett.py # Dataset generator with variations
├── hindi_names_dataset.csv # Generated names dataset
├── hindi_names_pairs_dataset.csv # Training pairs for model
├── hindi_name_matcher.pkl # Trained model object
├── server.py # Flask API server
├── static/
│ ├── index.html # Frontend UI
│ ├── app.js # Client-side JS logic
│ ├── model.js # Model interaction logic
│ ├── styles.css # Basic styling
│ └── apr-client.js # Optional client code
```
## ⚙️ How It Works

1. **Dataset Generation (`Namedatasett.py`)**  
   Creates synthetic variations of Hindi names using phonetic changes, typos, and transliteration rules.

2. **Feature Extraction (`matcher.py`)**  
   Extracts 20+ features between two names (e.g., Levenshtein distance, Soundex, common bigrams/trigrams).

3. **Model Training (`HindiNameMatcher.py`)**  
   Trains a Random Forest model and saves it as a `.pkl` file.

4. **Flask API (`server.py`)**  
   Provides `/api/compare`, `/api/search`, and `/api/feature-importance` endpoints.

---

## 🚀 Getting Started

### 1. Clone the repository:
```bash
git clone https://github.com/raj0401/Government-Name-Management-Portal.git
cd Government-Name-Management-Portal
2. Install dependencies:
bash
Copy
Edit
pip install -r requirements.txt
3. Train the model (optional if hindi_name_matcher.pkl exists):
bash
Copy
Edit
python HindiNameMatcher.py
4. Run the Flask server:
bash
Copy
Edit
python server.py
5. Open the browser:
Visit http://localhost:5000 to use the UI.

🧪 Example API Usage
POST /api/compare
json
Copy
Edit
{
  "name1": "Aditya Sharma",
  "name2": "Aditiya Sharma",
  "threshold": 0.5
}
POST /api/search
json
Copy
Edit
{
  "query_name": "Suresh Kumar",
  "candidate_names": ["Suresh Kumaar", "Ramesh Kumar", "Suresh Gupta"]
}
📊 Top Features Used
levenshtein_ratio

normalized_levenshtein_ratio

phonetic_matches (Soundex, Metaphone, NYSIIS)

n-gram overlap (bigrams, trigrams)

first/last name similarity

📦 Requirements
Python 3.7+

pandas, numpy, scikit-learn

Levenshtein, jellyfish, flask, pickle

🧠 Future Improvements
Integration with government databases

Multi-language support (Bengali, Tamil, etc.)

Admin dashboard for match validation and feedback learning

👨‍💻 Author
Shubham Raj – @raj0401

📄 License
MIT License – use freely with credit. Contributions welcome!

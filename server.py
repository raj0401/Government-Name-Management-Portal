from flask import Flask, request, jsonify, send_from_directory
import pickle
import os
import pandas as pd
from matcher import HindiNameMatcher, extract_features, feature_names

print(os.listdir('static'))

app = Flask(__name__, static_url_path='/static', static_folder='static')


# Load the model
try:
    with open("hindi_name_matcher.pkl", 'rb') as f:
        model = pickle.load(f)
    matcher = HindiNameMatcher(model)
    model_loaded = True
    print("Model loaded successfully!")
except FileNotFoundError:
    print("Model file not found. API will operate in demo mode.")
    model_loaded = False
except Exception as e:
    print(f"Error loading model: {e}")
    model_loaded = False

# Serve the main page
@app.route('/')
def index():
    return send_from_directory('static', 'index.html') 

@app.route('/api/compare', methods=['POST'])
def compare_names():
    """API endpoint to compare two names."""
    data = request.json
    name1 = data.get('name1', '')
    name2 = data.get('name2', '')
    threshold = float(data.get('threshold', 0.5))
    
    if not name1 or not name2:
        return jsonify({'error': 'Both names are required'}), 400
    
    if model_loaded:
        # Use the actual model
        result = matcher.predict_match(name1, name2, threshold)
        return jsonify(result)
    else:
        # Demo mode - use placeholder results
        import random
        import Levenshtein
        
        # Calculate basic similarity
        similarity = Levenshtein.ratio(name1.lower(), name2.lower())
        # Add some randomness for demo purposes
        confidence = min(1.0, max(0.0, similarity + random.uniform(-0.1, 0.1)))
        
        return jsonify({
            'is_match': confidence >= threshold,
            'confidence': confidence,
            'features': {
                'levenshtein_ratio': similarity,
                'note': 'This is a demo result. Features are simulated.'
            }
        })

@app.route('/api/search', methods=['POST'])
def search_names():
    """API endpoint to search for matching names."""
    data = request.json
    query_name = data.get('query_name', '')
    candidate_names = data.get('candidate_names', [])
    threshold = float(data.get('threshold', 0.5))
    
    if not query_name or not candidate_names:
        return jsonify({'error': 'Query name and candidate names are required'}), 400
    
    if model_loaded:
        # Use the actual model
        matches = matcher.find_matches(query_name, candidate_names, threshold)
        return jsonify({'matches': matches})
    else:
        # Demo mode - use placeholder results
        import random
        import Levenshtein
        
        matches = []
        for candidate in candidate_names:
            # Calculate basic similarity
            similarity = Levenshtein.ratio(query_name.lower(), candidate.lower())
            # Add some randomness for demo purposes
            confidence = min(1.0, max(0.0, similarity + random.uniform(-0.1, 0.1)))
            
            if confidence >= threshold:
                matches.append({
                    'name': candidate,
                    'confidence': confidence
                })
        
        # Sort by confidence
        matches.sort(key=lambda x: x['confidence'], reverse=True)
        
        return jsonify({'matches': matches})

@app.route('/api/feature-importance', methods=['GET'])
def feature_importance():
    """API endpoint to get feature importance data."""
    if model_loaded:
        # Get feature importance from the loaded model
        importances = {feature: float(importance) for feature, importance in 
                      zip(matcher.feature_names, matcher.model.feature_importances_)}
    else:
        # Demo data
        importances = {
            'levenshtein_ratio': 0.226,
            'normalized_levenshtein_ratio': 0.154,
            'first_levenshtein_ratio': 0.124,
            'last_levenshtein_ratio': 0.102,
            'soundex_match_first': 0.085,
            'common_bigrams': 0.063,
            'metaphone_match_first': 0.046,
            'nysiis_match_first': 0.043,
            'common_trigrams': 0.035,
            'len_ratio': 0.031,
            'first_letter_match': 0.024,
            'soundex_match_last': 0.022,
            'levenshtein_dist': 0.016,
            'metaphone_match_last': 0.014,
            'len_diff': 0.011,
            'first_levenshtein_dist': 0.010,
            'nysiis_match_last': 0.009,
            'has_first_transposition': 0.009,
            'last_first_letter_match': 0.008,
            'has_last_transposition': 0.007,
            'last_levenshtein_dist': 0.006
        }
    
    return jsonify({'feature_importance': importances})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
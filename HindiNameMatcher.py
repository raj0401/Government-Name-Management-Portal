import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import Levenshtein
import jellyfish
import re
from matcher import HindiNameMatcher

# Load the dataset
pairs_df = pd.read_csv("C:\\Users\\rajsu\\Desktop\\fuzzy_logic\\hindi_names_pairs_dataset.csv")

# Feature engineering function
def extract_features(name1, name2):
    """Extract features for comparing two names."""
    name1 = str(name1).lower()
    name2 = str(name2).lower()
    
    # Split into first name and last name
    name1_parts = name1.split()
    name2_parts = name2.split()
    
    # Get first and last names (handling cases with multiple name parts)
    name1_first = name1_parts[0] if name1_parts else ""
    name1_last = name1_parts[-1] if len(name1_parts) > 1 else ""
    
    name2_first = name2_parts[0] if name2_parts else ""
    name2_last = name2_parts[-1] if len(name2_parts) > 1 else ""
    
    # Basic distance features
    levenshtein_dist = Levenshtein.distance(name1, name2)
    levenshtein_ratio = Levenshtein.ratio(name1, name2)
    
    # First name distance features
    first_levenshtein_dist = Levenshtein.distance(name1_first, name2_first)
    first_levenshtein_ratio = Levenshtein.ratio(name1_first, name2_first)
    
    # Last name distance features
    last_levenshtein_dist = Levenshtein.distance(name1_last, name2_last)
    last_levenshtein_ratio = Levenshtein.ratio(name1_last, name2_last)
    
    # Phonetic features
    soundex_match_first = int(jellyfish.soundex(name1_first) == jellyfish.soundex(name2_first))
    soundex_match_last = int(jellyfish.soundex(name1_last) == jellyfish.soundex(name2_last))
    
    metaphone_match_first = int(jellyfish.metaphone(name1_first) == jellyfish.metaphone(name2_first))
    metaphone_match_last = int(jellyfish.metaphone(name1_last) == jellyfish.metaphone(name2_last))
    
    nysiis_match_first = int(jellyfish.nysiis(name1_first) == jellyfish.nysiis(name2_first))
    nysiis_match_last = int(jellyfish.nysiis(name1_last) == jellyfish.nysiis(name2_last))
    
    # Common Hindi transliteration patterns
    # Normalize common Hindi transliteration variations
    def normalize_hindi_transliterations(text):
        replacements = [
            ('aa', 'a'), ('ee', 'i'), ('oo', 'u'),
            ('sh', 's'), ('ph', 'f'), ('th', 't'),
            ('kh', 'k'), ('v', 'w')
        ]
        for old, new in replacements:
            text = text.replace(old, new)
        return text
    
    normalized_name1 = normalize_hindi_transliterations(name1)
    normalized_name2 = normalize_hindi_transliterations(name2)
    
    normalized_levenshtein_ratio = Levenshtein.ratio(normalized_name1, normalized_name2)
    
    # Common character sequences
    common_bigrams = len(set(re.findall(r'(?=(\w{2}))', name1)) & 
                         set(re.findall(r'(?=(\w{2}))', name2)))
    common_trigrams = len(set(re.findall(r'(?=(\w{3}))', name1)) &
                          set(re.findall(r'(?=(\w{3}))', name2)))
    
    # Starting letters match
    first_letter_match = int(name1_first[0] == name2_first[0]) if name1_first and name2_first else 0
    last_first_letter_match = int(name1_last[0] == name2_last[0]) if name1_last and name2_last else 0
    
    # Length-based features
    len_diff = abs(len(name1) - len(name2))
    len_ratio = min(len(name1), len(name2)) / max(len(name1), len(name2)) if max(len(name1), len(name2)) > 0 else 0
    
    # Check for transpositions
    def has_transposition(str1, str2):
        if abs(len(str1) - len(str2)) > 1:
            return 0
        
        for i in range(len(str1) - 1):
            transposed = str1[:i] + str1[i+1] + str1[i] + str1[i+2:] if i+2 < len(str1) else str1[:i] + str1[i+1] + str1[i]
            if transposed == str2:
                return 1
        return 0
    
    has_first_transposition = has_transposition(name1_first, name2_first)
    has_last_transposition = has_transposition(name1_last, name2_last)
    
    # Feature vector
    features = [
        levenshtein_dist, levenshtein_ratio, 
        first_levenshtein_dist, first_levenshtein_ratio,
        last_levenshtein_dist, last_levenshtein_ratio,
        soundex_match_first, soundex_match_last,
        metaphone_match_first, metaphone_match_last,
        nysiis_match_first, nysiis_match_last,
        normalized_levenshtein_ratio,
        common_bigrams, common_trigrams,
        first_letter_match, last_first_letter_match,
        len_diff, len_ratio,
        has_first_transposition, has_last_transposition
    ]
    
    return features

# Extract features for all pairs
print("Extracting features...")
X = []
for _, row in pairs_df.iterrows():
    features = extract_features(row['name1'], row['name2'])
    X.append(features)

X = np.array(X)
y = pairs_df['is_match'].values

# Split data
print("Splitting data into train and test sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest classifier
print("Training the model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
print("Evaluating the model...")
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")

# Feature importance
feature_names = [
    'levenshtein_dist', 'levenshtein_ratio', 
    'first_levenshtein_dist', 'first_levenshtein_ratio',
    'last_levenshtein_dist', 'last_levenshtein_ratio',
    'soundex_match_first', 'soundex_match_last',
    'metaphone_match_first', 'metaphone_match_last',
    'nysiis_match_first', 'nysiis_match_last',
    'normalized_levenshtein_ratio',
    'common_bigrams', 'common_trigrams',
    'first_letter_match', 'last_first_letter_match',
    'len_diff', 'len_ratio',
    'has_first_transposition', 'has_last_transposition'
]

importances = model.feature_importances_
indices = np.argsort(importances)[::-1]

print("\nFeature importances:")
for i in range(len(feature_names)):
    print(f"{feature_names[indices[i]]}: {importances[indices[i]]:.4f}")

# Create a wrapper class for the model
class HindiNameMatcher:
    def __init__(self, model):
        self.model = model
    
    def predict_match(self, name1, name2, threshold=0.5):
        """Predict if two names match."""
        features = extract_features(name1, name2)
        probability = self.model.predict_proba([features])[0][1]
        return {
            'is_match': probability >= threshold,
            'confidence': probability,
            'features': dict(zip(feature_names, features))
        }
    
    def find_matches(self, query_name, candidate_names, threshold=0.5):
        """Find all matches for a query name in a list of candidate names."""
        matches = []
        for candidate in candidate_names:
            result = self.predict_match(query_name, candidate, threshold)
            if result['is_match']:
                matches.append({
                    'name': candidate,
                    'confidence': result['confidence']
                })
        
        # Sort by confidence
        matches.sort(key=lambda x: x['confidence'], reverse=True)
        return matches

# Create the matcher instance
matcher = HindiNameMatcher(model)

# Save the model
with open("hindi_name_matcher_model.pkl", 'wb') as f:
    pickle.dump(model, f)

# Alternatively, save the entire matcher
with open("hindi_name_matcher.pkl", 'wb') as f:
    pickle.dump(matcher, f)

print("Model saved as hindi_name_matcher.pkl")

# Example usage
print("\nExample usage:")
test_cases = [
    ("Aditya Sharma", "Aditiya Sharma"),
    ("Rahul Singh", "Rahul Sing"),
    ("Suresh Kumar", "Sursh Kumaar"),
    ("Vikram Gupta", "Bikram Gupta"),
    ("Divya Mishra", "Divya Mishara"),
    ("Deepak Verma", "Dipak Varma"),
    ("Ananya Shah", "Ananya Sah")
]

for name1, name2 in test_cases:
    result = matcher.predict_match(name1, name2)
    print(f"{name1} vs {name2}: Match={result['is_match']}, Confidence={result['confidence']:.4f}")

# Test search functionality
test_query = "Suresh Kumar"
test_candidates = [
    "Suresh Kumar", "Sursh Kumaar", "Suresh Kumaar", 
    "Sresh Kumar", "Suresh Gupta", "Ramesh Kumar"
]

print("\nQuery:", test_query)
matches = matcher.find_matches(test_query, test_candidates)
print("Matches found:")
for match in matches:
    print(f"  {match['name']} (confidence: {match['confidence']:.4f})")
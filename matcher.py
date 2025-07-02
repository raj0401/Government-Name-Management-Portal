import Levenshtein
import jellyfish
import re
import numpy as np

# Define feature names for model
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

def normalize_hindi_transliterations(text):
    """Normalize common Hindi transliteration variations."""
    replacements = [
        ('aa', 'a'), ('ee', 'i'), ('oo', 'u'),
        ('sh', 's'), ('ph', 'f'), ('th', 't'),
        ('kh', 'k'), ('v', 'w')
    ]
    
    result = text
    for old, new in replacements:
        result = re.sub(old, new, result, flags=re.IGNORECASE)
    
    return result

def get_ngrams(text, n):
    """Extract n-grams from text."""
    return [text[i:i+n] for i in range(len(text) - n + 1)]

def common_ngrams(str1, str2, n):
    """Count common n-grams between two strings."""
    ngrams1 = set(get_ngrams(str1, n))
    ngrams2 = set(get_ngrams(str2, n))
    
    return len(ngrams1.intersection(ngrams2))

def has_transposition(str1, str2):
    """Check if strings differ by a single character transposition."""
    if abs(len(str1) - len(str2)) > 1:
        return 0
    
    for i in range(len(str1) - 1):
        transposed = str1[:i] + str1[i+1] + str1[i] + str1[i+2:]
        if transposed == str2:
            return 1
    
    return 0

def extract_features(name1, name2):
    """Extract features for comparing two names."""
    name1 = str(name1).lower()
    name2 = str(name2).lower()
    
    # Split into first name and last name
    name1_parts = name1.split()
    name2_parts = name2.split()
    
    # Get first and last names
    name1_first = name1_parts[0] if name1_parts else ''
    name1_last = name1_parts[-1] if len(name1_parts) > 1 else ''
    
    name2_first = name2_parts[0] if name2_parts else ''
    name2_last = name2_parts[-1] if len(name2_parts) > 1 else ''
    
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
    soundex_match_first = int(jellyfish.soundex(name1_first) == jellyfish.soundex(name2_first)) if name1_first and name2_first else 0
    soundex_match_last = int(jellyfish.soundex(name1_last) == jellyfish.soundex(name2_last)) if name1_last and name2_last else 0
    
    metaphone_match_first = int(jellyfish.metaphone(name1_first) == jellyfish.metaphone(name2_first)) if name1_first and name2_first else 0
    metaphone_match_last = int(jellyfish.metaphone(name1_last) == jellyfish.metaphone(name2_last)) if name1_last and name2_last else 0
    
    nysiis_match_first = int(jellyfish.nysiis(name1_first) == jellyfish.nysiis(name2_first)) if name1_first and name2_first else 0
    nysiis_match_last = int(jellyfish.nysiis(name1_last) == jellyfish.nysiis(name2_last)) if name1_last and name2_last else 0
    
    # Normalize transliterations
    normalized_name1 = normalize_hindi_transliterations(name1)
    normalized_name2 = normalize_hindi_transliterations(name2)
    
    normalized_levenshtein_ratio = Levenshtein.ratio(normalized_name1, normalized_name2)
    
    # Common character sequences
    common_bigrams_count = common_ngrams(name1, name2, 2)
    common_trigrams_count = common_ngrams(name1, name2, 3)
    
    # Starting letters match
    first_letter_match = int(name1_first and name2_first and name1_first[0] == name2_first[0])
    last_first_letter_match = int(name1_last and name2_last and name1_last[0] == name2_last[0])
    
    # Length-based features
    len_diff = abs(len(name1) - len(name2))
    len_ratio = min(len(name1), len(name2)) / max(len(name1), len(name2)) if max(len(name1), len(name2)) > 0 else 0
    
    # Transpositions
    has_first_transposition_val = has_transposition(name1_first, name2_first)
    has_last_transposition_val = has_transposition(name1_last, name2_last)
    
    # Return features as a list in the order defined in feature_names
    features = [
        levenshtein_dist, levenshtein_ratio,
        first_levenshtein_dist, first_levenshtein_ratio,
        last_levenshtein_dist, last_levenshtein_ratio,
        soundex_match_first, soundex_match_last,
        metaphone_match_first, metaphone_match_last,
        nysiis_match_first, nysiis_match_last,
        normalized_levenshtein_ratio,
        common_bigrams_count, common_trigrams_count,
        first_letter_match, last_first_letter_match,
        len_diff, len_ratio,
        has_first_transposition_val, has_last_transposition_val
    ]
    
    return features

class HindiNameMatcher:
    def __init__(self, model):
        self.model = model
        self.feature_names = feature_names

    def predict_match(self, name1, name2, threshold=0.5):
        features = extract_features(name1, name2)
        probability = self.model.predict_proba([features])[0][1]
        return {
            'is_match': probability >= threshold,
            'confidence': probability,
            'features': dict(zip(feature_names, features))
        }

    def find_matches(self, query_name, candidate_names, threshold=0.5):
        matches = []
        for candidate in candidate_names:
            result = self.predict_match(query_name, candidate, threshold)
            if result['is_match']:
                matches.append({
                    'name': candidate,
                    'confidence': result['confidence']
                })
        matches.sort(key=lambda x: x['confidence'], reverse=True)
        return matches
import pandas as pd
import numpy as np
import random
import string

# Set seed for reproducibility
np.random.seed(42)

# Common Hindi names (first names)
hindi_first_names = [
    "Aarav", "Aditya", "Amit", "Ananya", "Arjun", "Deepak", "Divya", "Gaurav", 
    "Ishaan", "Kavita", "Krishna", "Lakshmi", "Manish", "Neha", "Pooja", "Rahul", 
    "Ravi", "Sanjay", "Shreya", "Suresh", "Varun", "Vikram", "Yash"
]

# Common Hindi surnames
hindi_surnames = [
    "Sharma", "Patel", "Kumar", "Singh", "Gupta", "Verma", "Mishra", "Joshi", 
    "Chauhan", "Yadav", "Agarwal", "Mehta", "Choudhary", "Shah", "Trivedi"
]

# Functions to generate variations

def generate_transliteration_variation(name):
    """Generate common transliteration variations of Hindi names."""
    variations = {
        "aa": "a",
        "ee": "i",
        "oo": "u",
        "sh": "s",
        "ks": "x",
        "v": "w",
        "ph": "f",
        "th": "t",
        "kh": "k",
        "a": "aa",
        "i": "ee",
        "u": "oo"
    }
    
    # Choose one variation to apply
    possible_variations = []
    for old, new in variations.items():
        if old in name.lower():
            possible_variations.append((old, new))
    
    if not possible_variations:
        return name
    
    # Apply one random variation
    old, new = random.choice(possible_variations)
    return name.replace(old, new, 1)

def introduce_typo(name):
    """Introduce common typos in names."""
    if len(name) <= 2:
        return name
    
    typo_type = random.choice(['swap', 'drop', 'add', 'replace'])
    position = random.randint(1, len(name) - 1)
    
    if typo_type == 'swap' and position < len(name) - 1:
        chars = list(name)
        chars[position], chars[position + 1] = chars[position + 1], chars[position]
        return ''.join(chars)
    elif typo_type == 'drop':
        return name[:position] + name[position + 1:]
    elif typo_type == 'add':
        return name[:position] + random.choice(string.ascii_lowercase) + name[position:]
    else:  # replace
        return name[:position] + random.choice(string.ascii_lowercase) + name[position + 1:]

def generate_phonetic_variation(name):
    """Generate phonetic variations common in Hindi names."""
    phonetic_variations = {
        "v": "b",
        "w": "v",
        "f": "ph",
        "s": "sh",
        "z": "j",
        "t": "th",
        "d": "dh",
        "n": "nn",
        "m": "mm"
    }
    
    possible_variations = []
    for old, new in phonetic_variations.items():
        if old in name.lower():
            possible_variations.append((old, new))
    
    if not possible_variations:
        return name
    
    old, new = random.choice(possible_variations)
    return name.replace(old, new, 1)

# Generate dataset
num_samples = 1000
data = []

for _ in range(num_samples):
    # Create a standard name
    first_name = random.choice(hindi_first_names)
    last_name = random.choice(hindi_surnames)
    standard_name = f"{first_name} {last_name}"
    person_id = f"PID{random.randint(10000, 99999)}"
    
    # Add the standard entry
    data.append({
        'person_id': person_id,
        'name': standard_name,
        'name_type': 'standard',
        'case_id': f"C{random.randint(1000, 9999)}",
        'role': random.choice(['witness', 'suspect', 'victim', 'reporter']),
        'is_matching_pair': 1
    })
    
    # Add variations
    num_variations = random.randint(1, 3)
    for i in range(num_variations):
        variation_type = random.choice(['transliteration', 'typo', 'phonetic'])
        
        if variation_type == 'transliteration':
            varied_first = generate_transliteration_variation(first_name)
            varied_last = generate_transliteration_variation(last_name)
        elif variation_type == 'typo':
            varied_first = introduce_typo(first_name)
            varied_last = introduce_typo(last_name)
        else:  # phonetic
            varied_first = generate_phonetic_variation(first_name)
            varied_last = generate_phonetic_variation(last_name)
        
        varied_name = f"{varied_first} {varied_last}"
        
        data.append({
            'person_id': person_id,  # Same person_id indicates it's the same person
            'name': varied_name,
            'name_type': variation_type,
            'case_id': f"C{random.randint(1000, 9999)}",
            'role': random.choice(['witness', 'suspect', 'victim', 'reporter']),
            'is_matching_pair': 1
        })
    
    # Add some non-matching pairs for training
    if random.random() < 0.3:  # 30% chance to add a non-matching pair
        diff_first_name = random.choice([n for n in hindi_first_names if n != first_name])
        diff_last_name = random.choice([n for n in hindi_surnames if n != last_name])
        
        if random.random() < 0.5:
            non_match_name = f"{diff_first_name} {last_name}"
        else:
            non_match_name = f"{first_name} {diff_last_name}"
        
        data.append({
            'person_id': f"PID{random.randint(10000, 99999)}",  # Different person_id
            'name': non_match_name,
            'name_type': 'non_matching',
            'case_id': f"C{random.randint(1000, 9999)}",
            'role': random.choice(['witness', 'suspect', 'victim', 'reporter']),
            'is_matching_pair': 0
        })

# Create DataFrame and save to CSV
df = pd.DataFrame(data)

# Create pairs for training
pairs = []
for idx, row in df.iterrows():
    # For each name, create matching and non-matching pairs
    # Matching pairs (same person_id)
    matches = df[(df['person_id'] == row['person_id']) & (df.index != idx)]
    for _, match in matches.iterrows():
        pairs.append({
            'name1': row['name'],
            'name2': match['name'],
            'is_match': 1
        })
    
    # Non-matching pairs (different person_id)
    non_matches = df[(df['person_id'] != row['person_id'])]
    # Sample a few non-matches to keep dataset balanced
    non_matches_sample = non_matches.sample(min(2, len(non_matches)))
    for _, non_match in non_matches_sample.iterrows():
        pairs.append({
            'name1': row['name'],
            'name2': non_match['name'],
            'is_match': 0
        })

pairs_df = pd.DataFrame(pairs)

# Display sample from original dataset
print("Original Dataset Sample:")
print(df.head())
print(f"\nTotal records: {len(df)}")

# Display sample from pairs dataset
print("\nPairs Dataset Sample:")
print(pairs_df.head())
print(f"\nTotal pairs: {len(pairs_df)}")

# Save datasets
df.to_csv('hindi_names_dataset.csv', index=False)
pairs_df.to_csv('hindi_names_pairs_dataset.csv', index=False)

# Print counts
print("\nVariation Types:")
print(df['name_type'].value_counts())

print("\nRole Distribution:")
print(df['role'].value_counts())

print("\nMatch Distribution in Pairs:")
print(pairs_df['is_match'].value_counts())
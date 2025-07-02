/**
 * Hindi Name Matcher - Frontend Model Implementation
 * This file contains a JavaScript implementation of the Hindi Name Matcher model
 * based on the Python model provided in namematchingmodel.py
 */

// Simulated model implementation (in a real app, this would connect to a backend)
class HindiNameMatcher {
    constructor() {
        // Feature importances (from the Python model)
        this.featureImportance = {
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
        };
    }

    // Calculate Levenshtein distance between two strings
    levenshteinDistance(str1, str2) {
        const track = Array(str2.length + 1).fill(null).map(() => 
            Array(str1.length + 1).fill(null));
        
        for (let i = 0; i <= str1.length; i++) {
            track[0][i] = i;
        }
        
        for (let j = 0; j <= str2.length; j++) {
            track[j][0] = j;
        }
            
        for (let j = 1; j <= str2.length; j++) {
            for (let i = 1; i <= str1.length; i++) {
                const indicator = str1[i - 1] === str2[j - 1] ? 0 : 1;
                track[j][i] = Math.min(
                    track[j][i - 1] + 1, // deletion
                    track[j - 1][i] + 1, // insertion
                    track[j - 1][i - 1] + indicator // substitution
                );
            }
        }
        
        return track[str2.length][str1.length];
    }

    // Calculate Levenshtein ratio (similarity) between two strings
    levenshteinRatio(str1, str2) {
        const distance = this.levenshteinDistance(str1, str2);
        return 1 - (distance / Math.max(str1.length, str2.length));
    }

    // Simplified soundex implementation
    soundex(str) {
        if (!str) return '0000';
        
        // Convert to uppercase
        let s = str.toUpperCase();
        
        // Keep first letter
        let result = s[0];
        
        // Map of letters to soundex codes
        const codes = {
            'B': 1, 'F': 1, 'P': 1, 'V': 1,
            'C': 2, 'G': 2, 'J': 2, 'K': 2, 'Q': 2, 'S': 2, 'X': 2, 'Z': 2,
            'D': 3, 'T': 3,
            'L': 4,
            'M': 5, 'N': 5,
            'R': 6
        };
        
        // Previous code
        let prevCode = -1;
        
        // Process the rest of the string
        for (let i = 1; i < s.length; i++) {
            const code = codes[s[i]] || 0;
            
            // Skip vowels and 'H', 'W', 'Y' (code 0)
            // Skip duplicates
            if (code > 0 && code !== prevCode) {
                result += code;
            }
            
            prevCode = code;
            
            // Stop at 4 characters
            if (result.length >= 4) break;
        }
        
        // Pad with zeros if needed
        while (result.length < 4) {
            result += '0';
        }
        
        return result;
    }

    // Simplified metaphone implementation
    metaphone(str) {
        if (!str) return '';
        
        // Too complex for full implementation, simplified version
        return str.toLowerCase().replace(/[aeiou]/g, '').substring(0, 4);
    }

    // Simplified NYSIIS implementation
    nysiis(str) {
        if (!str) return '';
        
        // Too complex for full implementation, simplified version
        return str.toLowerCase().replace(/[aeiou]/g, '').substring(0, 4);
    }

    // Get common n-grams
    getNGrams(str, n) {
        const ngrams = [];
        for (let i = 0; i <= str.length - n; i++) {
            ngrams.push(str.substr(i, n));
        }
        return ngrams;
    }

    // Find common n-grams between two strings
    commonNGrams(str1, str2, n) {
        const ngrams1 = new Set(this.getNGrams(str1, n));
        const ngrams2 = new Set(this.getNGrams(str2, n));
        
        let common = 0;
        for (const gram of ngrams1) {
            if (ngrams2.has(gram)) {
                common++;
            }
        }
        
        return common;
    }

    // Check for transpositions
    hasTransposition(str1, str2) {
        if (Math.abs(str1.length - str2.length) > 1) {
            return 0;
        }
        
        for (let i = 0; i < str1.length - 1; i++) {
            const transposed = str1.substring(0, i) + str1[i+1] + str1[i] + str1.substring(i+2);
            if (transposed === str2) {
                return 1;
            }
        }
        
        return 0;
    }

    // Normalize common Hindi transliteration variations
    normalizeHindiTransliterations(text) {
        const replacements = [
            ['aa', 'a'], ['ee', 'i'], ['oo', 'u'],
            ['sh', 's'], ['ph', 'f'], ['th', 't'],
            ['kh', 'k'], ['v', 'w']
        ];
        
        let result = text;
        for (const [old, neo] of replacements) {
            result = result.replace(new RegExp(old, 'g'), neo);
        }
        
        return result;
    }

    // Extract features for comparing two names
    extractFeatures(name1, name2) {
        name1 = String(name1).toLowerCase();
        name2 = String(name2).toLowerCase();
        
        // Split into first name and last name
        const name1Parts = name1.split(' ');
        const name2Parts = name2.split(' ');
        
        // Get first and last names
        const name1First = name1Parts.length > 0 ? name1Parts[0] : '';
        const name1Last = name1Parts.length > 1 ? name1Parts[name1Parts.length - 1] : '';
        
        const name2First = name2Parts.length > 0 ? name2Parts[0] : '';
        const name2Last = name2Parts.length > 1 ? name2Parts[name2Parts.length - 1] : '';
        
        // Basic distance features
        const levenshteinDist = this.levenshteinDistance(name1, name2);
        const levenshteinRatio = this.levenshteinRatio(name1, name2);
        
        // First name distance features
        const firstLevenshteinDist = this.levenshteinDistance(name1First, name2First);
        const firstLevenshteinRatio = this.levenshteinRatio(name1First, name2First);
        
        // Last name distance features
        const lastLevenshteinDist = this.levenshteinDistance(name1Last, name2Last);
        const lastLevenshteinRatio = this.levenshteinRatio(name1Last, name2Last);
        
        // Phonetic features
        const soundexMatchFirst = this.soundex(name1First) === this.soundex(name2First) ? 1 : 0;
        const soundexMatchLast = this.soundex(name1Last) === this.soundex(name2Last) ? 1 : 0;
        
        const metaphoneMatchFirst = this.metaphone(name1First) === this.metaphone(name2First) ? 1 : 0;
        const metaphoneMatchLast = this.metaphone(name1Last) === this.metaphone(name2Last) ? 1 : 0;
        
        const nysiisMatchFirst = this.nysiis(name1First) === this.nysiis(name2First) ? 1 : 0;
        const nysiisMatchLast = this.nysiis(name1Last) === this.nysiis(name2Last) ? 1 : 0;
        
        // Normalize transliterations
        const normalizedName1 = this.normalizeHindiTransliterations(name1);
        const normalizedName2 = this.normalizeHindiTransliterations(name2);
        
        const normalizedLevenshteinRatio = this.levenshteinRatio(normalizedName1, normalizedName2);
        
        // Common character sequences
        const commonBigrams = this.commonNGrams(name1, name2, 2);
        const commonTrigrams = this.commonNGrams(name1, name2, 3);
        
        // Starting letters match
        const firstLetterMatch = name1First && name2First && name1First[0] === name2First[0] ? 1 : 0;
        const lastFirstLetterMatch = name1Last && name2Last && name1Last[0] === name2Last[0] ? 1 : 0;
        
        // Length-based features
        const lenDiff = Math.abs(name1.length - name2.length);
        const lenRatio = Math.min(name1.length, name2.length) / Math.max(name1.length, name2.length);
        
        // Transpositions
        const hasFirstTransposition = this.hasTransposition(name1First, name2First);
        const hasLastTransposition = this.hasTransposition(name1Last, name2Last);
        
        // Return features as an object
        return {
            levenshtein_dist: levenshteinDist,
            levenshtein_ratio: levenshteinRatio,
            first_levenshtein_dist: firstLevenshteinDist,
            first_levenshtein_ratio: firstLevenshteinRatio,
            last_levenshtein_dist: lastLevenshteinDist,
            last_levenshtein_ratio: lastLevenshteinRatio,
            soundex_match_first: soundexMatchFirst,
            soundex_match_last: soundexMatchLast,
            metaphone_match_first: metaphoneMatchFirst,
            metaphone_match_last: metaphoneMatchLast,
            nysiis_match_first: nysiisMatchFirst,
            nysiis_match_last: nysiisMatchLast,
            normalized_levenshtein_ratio: normalizedLevenshteinRatio,
            common_bigrams: commonBigrams,
            common_trigrams: commonTrigrams,
            first_letter_match: firstLetterMatch,
            last_first_letter_match: lastFirstLetterMatch,
            len_diff: lenDiff,
            len_ratio: lenRatio,
            has_first_transposition: hasFirstTransposition,
            has_last_transposition: hasLastTransposition
        };
    }

    // Predict if two names match using the extracted features
    predictMatch(name1, name2, threshold = 0.5) {
        const features = this.extractFeatures(name1, name2);
        
        // Calculate a weighted score based on feature importances
        let score = 0;
        for (const [feature, value] of Object.entries(features)) {
            if (feature in this.featureImportance) {
                score += value * this.featureImportance[feature];
            }
        }
        
        // Normalize score to 0-1 range
        const normalizedScore = Math.min(Math.max(score, 0), 1);
        
        return {
            is_match: normalizedScore >= threshold,
            confidence: normalizedScore,
            features: features
        };
    }

    // Find matches for a query name in a list of candidate names
    findMatches(queryName, candidateNames, threshold = 0.5) {
        const matches = [];
        
        for (const candidate of candidateNames) {
            const result = this.predictMatch(queryName, candidate, threshold);
            
            if (result.is_match) {
                matches.push({
                    name: candidate,
                    confidence: result.confidence
                });
            }
        }
        
        // Sort by confidence (descending)
        matches.sort((a, b) => b.confidence - a.confidence);
        
        return matches;
    }
}

// Create a singleton instance
const hindiNameMatcher = new HindiNameMatcher();
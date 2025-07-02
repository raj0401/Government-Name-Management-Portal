/**
 * Hindi Name Matcher - API Client
 * This file provides functions to communicate with the backend API
 */

// Base URL for API requests
const API_BASE_URL = '/api';

/**
 * Compare two names using the backend API
 * @param {string} name1 - First name to compare
 * @param {string} name2 - Second name to compare 
 * @param {number} threshold - Confidence threshold for matching
 * @returns {Promise} - Promise that resolves to the comparison result
 */
async function compareNamesAPI(name1, name2, threshold = 0.5) {
    try {
        const response = await fetch(`${API_BASE_URL}/compare`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name1, name2, threshold })
        });
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error comparing names:', error);
        // Fall back to client-side implementation
        return hindiNameMatcher.predictMatch(name1, name2, threshold);
    }
}

/**
 * Search for matching names using the backend API
 * @param {string} queryName - Name to search for
 * @param {Array<string>} candidateNames - List of candidate names to compare against
 * @param {number} threshold - Confidence threshold for matching
 * @returns {Promise} - Promise that resolves to the matches
 */
async function searchNamesAPI(queryName, candidateNames, threshold = 0.5) {
    try {
        const response = await fetch(`${API_BASE_URL}/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query_name: queryName, candidate_names: candidateNames, threshold })
        });
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        const data = await response.json();
        return data.matches;
    } catch (error) {
        console.error('Error searching names:', error);
        // Fall back to client-side implementation
        return hindiNameMatcher.findMatches(queryName, candidateNames, threshold);
    }
}

/**
 * Get feature importance data from the API
 * @returns {Promise} - Promise that resolves to the feature importance data
 */
async function getFeatureImportanceAPI() {
    try {
        const response = await fetch(`${API_BASE_URL}/feature-importance`);
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        const data = await response.json();
        return data.feature_importance;
    } catch (error) {
        console.error('Error getting feature importance:', error);
        // Fall back to client-side data
        return hindiNameMatcher.featureImportance;
    }
}
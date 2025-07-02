/**
 * Hindi Name Matcher - User Interface Logic
 * This file handles the interaction between the UI and the model
 */

// Initialize the chart
let featureChart = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Initialize threshold display
    const thresholdSlider = document.getElementById('threshold');
    const thresholdValue = document.getElementById('threshold-value');
    thresholdSlider.addEventListener('input', function() {
        thresholdValue.textContent = this.value;
    });

    const searchThresholdSlider = document.getElementById('search-threshold');
    const searchThresholdValue = document.getElementById('search-threshold-value');
    searchThresholdSlider.addEventListener('input', function() {
        searchThresholdValue.textContent = this.value;
    });

    // Initialize features chart
    initFeatureChart();

    // Load demo data
    loadDemoData();
});

// Tab switching functionality
function openTab(tabId) {
    // Hide all tab contents
    const tabContents = document.getElementsByClassName('tab-content');
    for (let i = 0; i < tabContents.length; i++) {
        tabContents[i].classList.remove('active');
    }
    
    // Deactivate all tab buttons
    const tabButtons = document.getElementsByClassName('tab-btn');
    for (let i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove('active');
    }
    
    // Show the selected tab content and activate its button
    document.getElementById(tabId).classList.add('active');
    document.querySelector(`button[onclick="openTab('${tabId}')"]`).classList.add('active');
}

// Compare two names
function compareNames() {
    const name1 = document.getElementById('name1').value.trim();
    const name2 = document.getElementById('name2').value.trim();
    const threshold = parseFloat(document.getElementById('threshold').value);
    
    // Validate inputs
    if (!name1 || !name2) {
        alert('Please enter both names to compare.');
        return;
    }
    
    // Get prediction
    const result = hindiNameMatcher.predictMatch(name1, name2, threshold);
    
    // Display result
    const resultBox = document.getElementById('compare-result');
    const matchText = document.getElementById('match-text');
    const confidenceValue = document.getElementById('confidence-value');
    const confidenceBar = document.getElementById('confidence-bar');
    
    resultBox.style.display = 'block';
    
    if (result.is_match) {
        matchText.textContent = 'MATCH';
        matchText.className = 'match-result match';
    } else {
        matchText.textContent = 'NO MATCH';
        matchText.className = 'match-result no-match';
    }
    
    confidenceValue.textContent = (result.confidence * 100).toFixed(2) + '%';
    confidenceBar.style.width = (result.confidence * 100) + '%';
    
    // Display features breakdown
    displayFeatures(result.features);
}

// Display feature breakdown
function displayFeatures(features) {
    const featuresDiv = document.getElementById('features-breakdown');
    featuresDiv.innerHTML = '';
    featuresDiv.style.display = 'block';
    
    // Get feature importance for sorting
    const importance = hindiNameMatcher.featureImportance;
    
    // Sort features by importance
    const sortedFeatures = Object.entries(features)
        .sort((a, b) => (importance[b[0]] || 0) - (importance[a[0]] || 0));
    
    // Create feature display
    for (const [feature, value] of sortedFeatures) {
        const featureDiv = document.createElement('div');
        featureDiv.className = 'feature-item';
        
        const nameSpan = document.createElement('span');
        nameSpan.className = 'feature-name';
        nameSpan.textContent = formatFeatureName(feature);
        
        const valueSpan = document.createElement('span');
        valueSpan.className = 'feature-value';
        valueSpan.textContent = typeof value === 'number' ? 
            value.toFixed(4) : 
            value.toString();
        
        featureDiv.appendChild(nameSpan);
        featureDiv.appendChild(valueSpan);
        featuresDiv.appendChild(featureDiv);
    }
}

// Format feature name for display
function formatFeatureName(feature) {
    return feature
        .replace(/_/g, ' ')
        .replace(/\b\w/g, l => l.toUpperCase());
}

// Search for name matches
function searchNames() {
    const queryName = document.getElementById('query-name').value.trim();
    const candidateNamesText = document.getElementById('candidate-names').value.trim();
    const threshold = parseFloat(document.getElementById('search-threshold').value);
    
    // Validate inputs
    if (!queryName || !candidateNamesText) {
        alert('Please enter a query name and candidate names.');
        return;
    }
    
    // Parse candidate names (one per line)
    const candidateNames = candidateNamesText
        .split('\n')
        .map(name => name.trim())
        .filter(name => name.length > 0);
    
    if (candidateNames.length === 0) {
        alert('Please enter at least one candidate name.');
        return;
    }
    
    // Find matches
    const matches = hindiNameMatcher.findMatches(queryName, candidateNames, threshold);
    
    // Display results
    const resultsDiv = document.getElementById('search-results');
    const matchesList = document.getElementById('matches-list');
    
    resultsDiv.style.display = 'block';
    matchesList.innerHTML = '';
    
    if (matches.length === 0) {
        matchesList.innerHTML = '<p>No matches found.</p>';
        return;
    }
    
    // Create matches display
    for (const match of matches) {
        const matchDiv = document.createElement('div');
        matchDiv.className = 'match-item';
        
        const nameSpan = document.createElement('span');
        nameSpan.textContent = match.name;
        
        const confidenceContainer = document.createElement('div');
        confidenceContainer.className = 'confidence-container';
        
        const confidenceLabel = document.createElement('span');
        confidenceLabel.textContent = (match.confidence * 100).toFixed(2) + '%';
        
        const confidenceBarContainer = document.createElement('div');
        confidenceBarContainer.className = 'confidence-bar';
        
        const confidenceBarLevel = document.createElement('div');
        confidenceBarLevel.className = 'confidence-level';
        confidenceBarLevel.style.width = (match.confidence * 100) + '%';
        
        confidenceBarContainer.appendChild(confidenceBarLevel);
        confidenceContainer.appendChild(confidenceLabel);
        confidenceContainer.appendChild(confidenceBarContainer);
        
        matchDiv.appendChild(nameSpan);
        matchDiv.appendChild(confidenceContainer);
        matchesList.appendChild(matchDiv);
    }
}

// Initialize the feature importance chart
function initFeatureChart() {
    const ctx = document.getElementById('feature-chart').getContext('2d');
    
    // Get feature importance data
    const importance = hindiNameMatcher.featureImportance;
    
    // Sort features by importance
    const sortedFeatures = Object.entries(importance)
        .sort((a, b) => b[1] - a[1]);
    
    const labels = sortedFeatures.map(([feature, _]) => formatFeatureName(feature));
    const data = sortedFeatures.map(([_, value]) => value);
    
    // Create chart
    featureChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Feature Importance',
                data: data,
                backgroundColor: 'rgba(92, 45, 145, 0.7)',
                borderColor: 'rgba(92, 45, 145, 1)',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return (context.raw * 100).toFixed(2) + '%';
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Importance Score'
                    }
                }
            }
        }
    });
}

// Load demo data
function loadDemoData() {
    // Demo data for comparison
    document.getElementById('name1').value = 'Vikram Gupta';
    document.getElementById('name2').value = 'Bikram Gupta';
    
    // Demo data for search
    document.getElementById('query-name').value = 'Suresh Kumar';
    document.getElementById('candidate-names').value = `Suresh Kumar
Sursh Kumaar
Suresh Kumaar
Sresh Kumar
Suresh Gupta
Ramesh Kumar`;
}
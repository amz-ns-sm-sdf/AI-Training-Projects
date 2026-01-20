const API_URL = 'http://localhost:5009/api';
let currentRuleSet = 'Product Photo';

async function loadRuleSets() {
    try {
        const response = await fetch(`${API_URL}/rule-sets`);
        const data = await response.json();
        
        const ruleSetsList = document.getElementById('ruleSets');
        let html = '';
        data.rule_sets.forEach(rs => {
            html += `
                <div class="rule-set-item ${rs.name === 'Product Photo' ? 'active' : ''}" 
                     onclick="selectRuleSet('${rs.name}')">
                    <div class="rule-set-name">${rs.name}</div>
                    <div class="rule-set-desc">${rs.description}</div>
                </div>
            `;
        });
        ruleSetsList.innerHTML = html;
    } catch (error) {
        console.error('Error loading rule sets:', error);
    }
}

async function selectRuleSet(name) {
    currentRuleSet = name;
    document.querySelectorAll('.rule-set-item').forEach(el => el.classList.remove('active'));
    event.target.closest('.rule-set-item').classList.add('active');
    await loadRules(name);
    document.getElementById('validationResult').innerHTML = '';
}

async function loadRules(ruleSet) {
    try {
        const response = await fetch(`${API_URL}/rules/${ruleSet}`);
        const data = await response.json();
        
        const rulesList = document.getElementById('rulesList');
        let html = '';
        data.rules.forEach(rule => {
            html += `<div class="rule-item">✓ ${rule}</div>`;
        });
        rulesList.innerHTML = html;
    } catch (error) {
        console.error('Error loading rules:', error);
    }
}

async function loadSampleImages() {
    try {
        const response = await fetch(`${API_URL}/sample-images`);
        const data = await response.json();
        
        const samplesDiv = document.getElementById('sampleImages');
        let html = '';
        data.samples.forEach(sample => {
            html += `
                <button class="sample-image-btn" 
                        onclick="useSample('${sample.url}', '${sample.rule_set}')">
                    ${sample.name}
                </button>
            `;
        });
        samplesDiv.innerHTML = html;
    } catch (error) {
        console.error('Error loading samples:', error);
    }
}

function useSample(url, ruleSet) {
    currentRuleSet = ruleSet;
    document.getElementById('imageUrl').value = url;
    document.getElementById('previewImage').src = url;
    selectRuleSet(ruleSet);
    validateImage();
}

async function validateImage() {
    const imageUrl = document.getElementById('imageUrl').value;
    
    if (!imageUrl) {
        alert('Please enter image URL');
        return;
    }
    
    document.getElementById('previewImage').src = imageUrl;
    
    try {
        const response = await fetch(`${API_URL}/validate-image`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                rule_set: currentRuleSet,
                image_url: imageUrl
            })
        });
        
        const data = await response.json();
        if (response.ok) {
            displayValidationResult(data.result);
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        alert('Error: ' + error);
    }
}

function displayValidationResult(result) {
    const resultDiv = document.getElementById('validationResult');
    const scoreColor = result.overall_score >= 60 ? '#4caf50' : '#f5576c';
    
    let html = `
        <div class="result-header">
            <span>Validation Results</span>
            <span style="margin-left: auto; color: ${scoreColor}; font-size: 20px;">
                ${result.passed ? '✓ APPROVED' : '✗ REJECTED'}
            </span>
        </div>
        <div class="score-display" style="color: ${scoreColor};">${result.overall_score}%</div>
        
        <div class="validations-list">
    `;
    
    result.validations.forEach(v => {
        const className = v.passed ? 'passed' : 'failed';
        const icon = v.passed ? '✓' : '✗';
        html += `
            <div class="validation-check ${className}">
                <span class="check-icon">${icon}</span>
                <span>${v.rule}</span>
            </div>
        `;
    });
    
    html += '</div>';
    
    if (result.issues.length > 0) {
        html += '<div style="margin-top: 15px;"><strong>Issues Found:</strong><ul>';
        result.issues.forEach(issue => {
            html += `<li>${issue}</li>`;
        });
        html += '</ul></div>';
    }
    
    const recClass = result.passed ? 'approved' : 'rejected';
    html += `<div class="recommendation ${recClass}">${result.recommendation}</div>`;
    
    resultDiv.innerHTML = html;
}

window.addEventListener('load', () => {
    loadRuleSets();
    loadRules('Product Photo');
    loadSampleImages();
});

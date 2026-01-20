from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import io

app = Flask(__name__)
CORS(app)

# Define rules
VALIDATION_RULES = {
    'Product Photo': {
        'rules': [
            'Image must have white background',
            'Product must be centered',
            'High quality and clear visibility',
            'No text or watermarks',
            'Square format (1:1 ratio)'
        ]
    },
    'ID Document': {
        'rules': [
            'Document must be fully visible',
            'Good lighting and contrast',
            'No glare or shadows',
            'Text must be readable',
            'All four corners must be visible'
        ]
    },
    'Selfie': {
        'rules': [
            'Face must occupy 50-70% of image',
            'Clear facial features',
            'Good lighting on face',
            'No filters or heavy editing',
            'Plain background preferred'
        ]
    }
}

# Mock image validation
def validate_image(image_data, rule_set):
    """Simulate image validation against rules"""
    # In real scenario, this would use computer vision
    # For demo, we return simulated validation results
    
    validations = []
    score = 100
    issues = []
    
    # Simulate checks based on rule set
    rules = VALIDATION_RULES.get(rule_set, {}).get('rules', [])
    
    for i, rule in enumerate(rules):
        # Mock validation: 80% pass rate
        passed = (i % 5) != 0
        validations.append({
            'rule': rule,
            'passed': passed,
            'details': f"{'✓ Pass' if passed else '✗ Fail'}: {rule}"
        })
        if not passed:
            score -= 20
            issues.append(rule)
    
    return {
        'rule_set': rule_set,
        'validations': validations,
        'overall_score': max(0, score),
        'passed': score >= 60,
        'issues': issues,
        'recommendation': 'Image approved' if score >= 60 else 'Please retake the image'
    }

@app.route('/api/rule-sets', methods=['GET'])
def get_rule_sets():
    """Get available rule sets"""
    return jsonify({
        "rule_sets": [
            {
                'name': 'Product Photo',
                'description': 'Rules for product catalog photos'
            },
            {
                'name': 'ID Document',
                'description': 'Rules for identity document verification'
            },
            {
                'name': 'Selfie',
                'description': 'Rules for selfie/portrait photos'
            }
        ]
    })

@app.route('/api/rules/<rule_set>', methods=['GET'])
def get_rules(rule_set):
    """Get specific rule set"""
    if rule_set not in VALIDATION_RULES:
        return jsonify({"error": "Rule set not found"}), 404
    
    return jsonify({
        "rule_set": rule_set,
        "rules": VALIDATION_RULES[rule_set]['rules']
    })

@app.route('/api/validate-image', methods=['POST'])
def validate():
    """Validate image against rules"""
    try:
        data = request.json
        rule_set = data.get('rule_set', '')
        image_url = data.get('image_url', '')
        
        if not rule_set:
            return jsonify({"error": "Rule set required"}), 400
        
        if rule_set not in VALIDATION_RULES:
            return jsonify({"error": "Unknown rule set"}), 404
        
        result = validate_image(image_url, rule_set)
        
        return jsonify({
            "status": "success",
            "result": result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/sample-images', methods=['GET'])
def get_sample_images():
    """Get sample image URLs for testing"""
    return jsonify({
        "samples": [
            {
                "name": "Product Example 1",
                "url": "https://via.placeholder.com/500x500/ffffff/000000?text=Laptop+Product",
                "rule_set": "Product Photo"
            },
            {
                "name": "ID Document Example",
                "url": "https://via.placeholder.com/600x400/cccccc/000000?text=ID+Document",
                "rule_set": "ID Document"
            },
            {
                "name": "Selfie Example",
                "url": "https://via.placeholder.com/400x400/ffffff/000000?text=Portrait+Photo",
                "rule_set": "Selfie"
            }
        ]
    })

if __name__ == '__main__':
    app.run(debug=False, port=5009, use_reloader=False)

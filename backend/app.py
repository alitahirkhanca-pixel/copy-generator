"""
Flask API Server for Email Copy Automation
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from copy_engine import generate_copy

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests


@app.route('/api/generate', methods=['POST'])
def generate():
    """
    Generate email copy variations.
    
    Expects JSON body:
    {
        "clientName": "Acme Corp",
        "industry": "SaaS",
        "audience": "Small Business Owners",
        "website": "https://acme.com",
        "strategy": "Focus on automation pain points..."
    }
    
    Returns:
    {
        "variations": [
            { "id": 1, "hookType": "...", "subject": "...", "body": "...", "ps": "..." },
            ...
        ]
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required = ['clientName', 'industry', 'website', 'strategy']
        missing = [f for f in required if not data.get(f)]
        if missing:
            return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400
        
        # Generate copy
        result = generate_copy(
            client_name=data.get('clientName'),
            industry=data.get('industry'),
            audience=data.get('audience', ''),
            website=data.get('website'),
            strategy=data.get('strategy')
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok"})


import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f"🚀 Copy Engine API running on port {port}")
    print("   POST /api/generate - Generate email variations")
    print("   GET  /api/health   - Health check")
    app.run(host='0.0.0.0', debug=False, port=port)


"""
Flask API Server for Email Copy Automation
Serves both the API and static frontend files.
"""

import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from copy_engine import generate_copy

# Get the parent directory where frontend files are
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

app = Flask(__name__, static_folder=FRONTEND_DIR)
CORS(app)  # Enable CORS for frontend requests


# ============ FRONTEND ROUTES ============

@app.route('/')
def index():
    """Serve the main frontend page."""
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    """Serve static files (CSS, JS, etc.)."""
    # Don't serve API routes as static
    if path.startswith('api/'):
        return jsonify({"error": "Not found"}), 404
    try:
        return send_from_directory(FRONTEND_DIR, path)
    except:
        return send_from_directory(FRONTEND_DIR, 'index.html')


# ============ API ROUTES ============

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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f"🚀 Psychic Copy Generator running on port {port}")
    print(f"   Frontend: http://localhost:{port}/")
    print(f"   API:      http://localhost:{port}/api/generate")
    app.run(host='0.0.0.0', debug=False, port=port)



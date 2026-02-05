from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Flask
app = Flask(__name__)

# CORS configuration
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["*"],
        "allow_headers": ["*"],
        "supports_credentials": True
    }
})

@app.route("/")
def root():
    return jsonify({
        "status": "success",
        "service": "Webhook Receiver",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": {
            "webhook": "/webhook (POST)",
            "health": "/health"
        }
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Received callback:", data)
    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    # Get port from environment variable, default to 9000
    port = int(os.getenv("PORT", 9000))
    
    print("🚀 Starting Webhook Receiver...")
    print(f"✅ Server ready on port {port}")
    
    # Run with production-ready settings
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,  # Set to False for production
        threaded=True  # Enable threading for concurrent requests
    )

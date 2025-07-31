from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "✅ Flask backend is live"

@app.route('/stock')
def get_stock_data():
    symbol = request.args.get('symbol', 'AAPL').upper()

    # Replace this with a real API call if you have a paid API key
    fake_data = {
        "symbol": symbol,
        "name": "Apple Inc." if symbol == "AAPL" else "Unknown",
        "price": "209.05",
        "open": "208.38",
        "high": "209.84",
        "low": "207.16",
        "previous_close": "209.05",
        "timestamp": 1753968600
    }

    return jsonify(fake_data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

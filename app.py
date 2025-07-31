from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Load your Finnhub API key from environment
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

# 🔁 Health check route for Render
@app.route('/')
def home():
    return "✅ Flask backend is live"

@app.route('/health')
def health():
    return "OK", 200

# 📈 Stock data route
@app.route('/stock')
def get_stock():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"error": "No symbol provided"}), 400

    try:
        # API requests
        profile_url = f"https://finnhub.io/api/v1/stock/profile2?symbol={symbol}&token={FINNHUB_API_KEY}"
        quote_url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"

        profile_res = requests.get(profile_url).json()
        quote_res = requests.get(quote_url).json()

        # Handle invalid symbol or empty data
        if "name" not in profile_res or not profile_res["name"]:
            return jsonify({"error": "Invalid stock symbol"}), 404

        return jsonify({
            "symbol": symbol,
            "name": profile_res.get("name"),
            "price": str(quote_res.get("c")),
            "open": str(quote_res.get("o")),
            "high": str(quote_res.get("h")),
            "low": str(quote_res.get("l")),
            "previous_close": str(quote_res.get("pc")),
            "timestamp": quote_res.get("t")
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

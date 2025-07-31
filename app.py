from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

@app.route('/')
def home():
    return "✅ Stock API backend is running"

@app.route('/stock')
def get_stock():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"error": "No symbol provided"}), 400

    try:
        profile_url = f"https://finnhub.io/api/v1/stock/profile2?symbol={symbol}&token={FINNHUB_API_KEY}"
        quote_url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"

        profile_res = requests.get(profile_url).json()
        quote_res = requests.get(quote_url).json()

        if "name" not in profile_res:
            return jsonify({"error": "Invalid symbol or no data"}), 404

        return jsonify({
            "symbol": symbol,
            "name": profile_res.get("name"),
            "price": quote_res.get("c"),
            "open": quote_res.get("o"),
            "high": quote_res.get("h"),
            "low": quote_res.get("l"),
            "previous_close": quote_res.get("pc"),
            "timestamp": quote_res.get("t")
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, jsonify, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

API_KEY = os.getenv("TWELVE_API_KEY")

@app.route('/stock', methods=['GET'])
def get_stock_data():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"error": "Symbol is required"}), 400

    url = f"https://api.twelvedata.com/quote?symbol={symbol}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "code" in data:
        return jsonify({"error": data.get("message", "API error")}), 500

    return jsonify({
    "symbol": data.get("symbol"),
    "name": data.get("name"),
    "price": data.get("price") or data.get("previous_close"),  # 👈 FIXED LINE
    "open": data.get("open"),
    "high": data.get("high"),
    "low": data.get("low"),
    "previous_close": data.get("previous_close"),
    "timestamp": data.get("timestamp")
})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

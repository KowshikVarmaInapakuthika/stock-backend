import React, { useState } from 'react';
import './App.css';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
} from 'chart.js';

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement);

function App() {
  const [symbol, setSymbol] = useState('');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchStock = async () => {
    if (!symbol) return;
    setLoading(true);
    try {
      const response = await fetch(`https://stock-backend-izs0.onrender.com/stock?symbol=${symbol}`);
      const json = await response.json();
      setData(json);
    } catch (err) {
      console.error("Fetch error:", err);
      setData({ error: "Something went wrong." });
    } finally {
      setLoading(false);
    }
  };

  const chartData = data && !data.error ? {
    labels: ['Open', 'High', 'Low', 'Previous Close'],
    datasets: [
      {
        label: `Price for ${symbol.toUpperCase()}`,
        data: [
          parseFloat(data.open),
          parseFloat(data.high),
          parseFloat(data.low),
          parseFloat(data.previous_close)
        ],
        borderColor: 'teal',
        backgroundColor: 'rgba(0,128,128,0.1)',
        fill: true,
        tension: 0.3,
      },
    ],
  } : null;

  return (
    <div className="App">
      <h1>📈 Real-Time Stock Tracker</h1>
      <input
        placeholder="Enter Stock Symbol (e.g., AAPL)"
        value={symbol}
        onChange={(e) => setSymbol(e.target.value)}
      />
      <button onClick={fetchStock}>Fetch Stock</button>

      {loading && <p>Loading...</p>}

      {data && !data.error && (
        <div>
          <h2>{data.name} ({data.symbol})</h2>
          <p><strong>Current Price:</strong> ${data.price}</p>
          {chartData && <Line data={chartData} />}
        </div>
      )}

      {data?.error && <p style={{ color: 'red' }}>❌ {data.error}</p>}
    </div>
  );
}

export default App;

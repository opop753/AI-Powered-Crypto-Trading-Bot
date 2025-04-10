import React, { useState, useEffect } from 'react';
import './App.css';
import CombinedData from './CombinedData';  // Import the CombinedData component

function App() {
  const [bitvavoData, setBitvavoData] = useState(null);
  const [yahooData, setYahooData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    console.log("Fetching data from API...");
    try {
      const responseBitvavo = await fetch('/api/bitvavo', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      const responseYahoo = await fetch('/api/price-data/yahoo');
      
      const resultBitvavo = await responseBitvavo.json();
      const resultYahoo = await responseYahoo.json();
      console.log("Data fetched successfully:", resultBitvavo, resultYahoo);
      setBitvavoData(resultBitvavo);
      setYahooData(resultYahoo.data); // Assuming the Yahoo data is in a 'data' field
    } catch (error) {
      setError(`Error fetching data: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header" style={{ position: 'relative', zIndex: 1 }}>
        <button onClick={fetchData}>Fetch Data</button>
        {loading && <p>Loading...</p>}
        {error && <p>Error: {error}</p>}
        
        {bitvavoData && Array.isArray(bitvavoData) && (
          <div>
            <h2>Bitvavo Market Data:</h2>
            <table>
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>Price</th>
                  <th>Volume</th>
                </tr>
              </thead>
              <tbody>
                {bitvavoData.map((item) => (
                  <tr key={item.timestamp}>
                    <td>{item.timestamp}</td>
                    <td>{item.price}</td>
                    <td>{item.volume}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {yahooData && Array.isArray(yahooData) && (
          <div>
            <h2>Yahoo Finance Data:</h2>
            <table>
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>Price</th>
                  <th>Volume</th>
                </tr>
              </thead>
              <tbody>
                {yahooData.map((item) => (
                  <tr key={item.timestamp}>
                    <td>{item.timestamp}</td>
                    <td>{item.price}</td>
                    <td>{item.volume}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        
        <CombinedData />  // Render the CombinedData component
        <p>
          Edit <code>src/App.js</code> and save to reload. 
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;

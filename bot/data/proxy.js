const express = require('express');
const cors = require('cors');
const allowedOrigins = ['http://localhost:3000', 'http://localhost:34155', 'http://localhost:8000']; // Add new frontend origin
const axios = require('axios');
const app = express();
app.use(cors({
    origin: ['http://localhost:3000', 'http://localhost:34155'] // Allow requests from both frontend origins
})); // Enable CORS for all routes
const PORT = 5000;

app.use(express.json());

app.post('/api/bitvavo', async (req, res) => {
    const { symbol, interval, start_date, end_date } = req.body;
    try {
        const response = await axios.get('https://api.bitvavo.com/v2/tickers', { 
            params: {
                market: symbol,
                interval: interval,
                start: start_date,
                end: end_date
            }
        });
        res.json(response.data);
    } catch (error) {
        console.error('Error fetching data from Bitvavo:', error);
        res.status(500).send('Error fetching data');
    }
});

app.listen(PORT, () => {
    console.log(`Proxy server running on http://localhost:${PORT}`);
});

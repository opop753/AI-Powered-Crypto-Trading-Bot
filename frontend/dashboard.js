// Check if user is logged in
document.addEventListener('DOMContentLoaded', () => {
    // Get stored username from cookies or localStorage
    const username = getCookie('username') || localStorage.getItem('username');
    
    if (username) {
        document.getElementById('username-display').textContent = `Welcome, ${username}`;
    } else {
        // If not logged in, redirect to login page
        // Uncomment this when authentication is fully implemented
        // window.location.href = '/login.html';
    }
    
    // Set up event listeners
    setupEventListeners();
});

// Helper function to get cookie value
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Setup all event listeners
function setupEventListeners() {
    // Fetch data button
    document.getElementById('fetch-data').addEventListener('click', fetchMarketData);
    
    // Train model button
    document.getElementById('train-model').addEventListener('click', trainModel);
    
    // Predict button
    document.getElementById('predict').addEventListener('click', makePrediction);
}

// Chart instance
let priceChart;

// Fetch market data from API
async function fetchMarketData() {
    const market = document.getElementById('market').value;
    const interval = document.getElementById('interval').value;
    
    // Calculate time range (last 24 hours by default)
    const endTime = Date.now();
    const startTime = endTime - (24 * 60 * 60 * 1000); // 24 hours ago
    
    try {
        // Show loading indicator
        document.getElementById('trading-chart').innerHTML = '<p>Loading data...</p>';
        
        // Fetch data from the API
        const response = await fetch(`/api/binance/candlestick?market=${market}&interval=${interval}&start_time=${startTime}&end_time=${endTime}`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch market data');
        }
        
        const data = await response.json();
        renderChart(data, market);
    } catch (error) {
        console.error('Error fetching market data:', error);
        document.getElementById('trading-chart').innerHTML = `<p>Error: ${error.message}</p>`;
    }
}

// Render price chart
function renderChart(data, market) {
    // Clear previous chart if it exists
    if (priceChart) {
        priceChart.destroy();
    }
    
    // Extract data for chart
    const labels = data.map(item => new Date(item[0]).toLocaleTimeString());
    const prices = data.map(item => parseFloat(item[4])); // Close prices
    
    // Create canvas for chart if it doesn't exist
    const chartContainer = document.getElementById('trading-chart');
    chartContainer.innerHTML = '';
    const canvas = document.createElement('canvas');
    canvas.id = 'price-chart-canvas';
    chartContainer.appendChild(canvas);
    
    // Create chart
    const ctx = canvas.getContext('2d');
    priceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: `${market} Price`,
                data: prices,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1,
                pointRadius: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}

// Train selected model
async function trainModel() {
    const model = document.getElementById('model').value;
    const market = document.getElementById('market').value;
    const interval = document.getElementById('interval').value;
    
    // Calculate time range (last 30 days for training)
    const endTime = Date.now();
    const startTime = endTime - (30 * 24 * 60 * 60 * 1000); // 30 days ago
    
    try {
        // Show loading message
        document.getElementById('prediction-results').innerHTML = '<p>Training model, please wait...</p>';
        
        // Fetch training data
        const response = await fetch(`/api/fetch/binance?market=${market}&interval=${interval}&start_time=${startTime}&end_time=${endTime}`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch training data');
        }
        
        const data = await response.json();
        
        // Prepare training data (simplified for demonstration)
        // In a real application, you would do more sophisticated preprocessing
        const X_train = data.map(item => [
            parseFloat(item[1]), // Open
            parseFloat(item[2]), // High
            parseFloat(item[3]), // Low
            parseFloat(item[4]), // Close
            parseFloat(item[5])  // Volume
        ]);
        
        const y_train = data.map((item, index) => {
            // Predict if next price is higher (1) or lower (0) than current
            if (index < data.length - 1) {
                return parseFloat(data[index + 1][4]) > parseFloat(item[4]) ? 1 : 0;
            }
            return 0; // Default for last item
        });
        
        // Send training data to backend
        const trainResponse = await fetch(`/api/train_${model}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ X_train, y_train })
        });
        
        if (!trainResponse.ok) {
            throw new Error('Failed to train model');
        }
        
        const trainResult = await trainResponse.json();
        document.getElementById('prediction-results').innerHTML = `<p>${trainResult.message}</p>`;
    } catch (error) {
        console.error('Error training model:', error);
        document.getElementById('prediction-results').innerHTML = `<p>Error: ${error.message}</p>`;
    }
}

// Make prediction with trained model
async function makePrediction() {
    const model = document.getElementById('model').value;
    const market = document.getElementById('market').value;
    
    try {
        // Show loading message
        document.getElementById('prediction-results').innerHTML = '<p>Making prediction, please wait...</p>';
        
        // In a real application, you would send the latest data for prediction
        // For demonstration, we'll use a simple request
        const response = await fetch(`/api/predict/${model}?market=${market}`);
        
        if (!response.ok) {
            throw new Error('Failed to make prediction');
        }
        
        const result = await response.json();
        
        // Display prediction result
        let predictionText = '';
        if (result.prediction === 1) {
            predictionText = `<p class="prediction up">Prediction: Price likely to ⬆️ INCREASE</p>`;
        } else {
            predictionText = `<p class="prediction down">Prediction: Price likely to ⬇️ DECREASE</p>`;
        }
        
        document.getElementById('prediction-results').innerHTML = `
            <div>
                ${predictionText}
                <p>Confidence: ${(result.confidence * 100).toFixed(2)}%</p>
                <p>Model: ${model.toUpperCase()}</p>
                <p>Market: ${market}</p>
                <p>Time: ${new Date().toLocaleString()}</p>
            </div>
        `;
    } catch (error) {
        console.error('Error making prediction:', error);
        document.getElementById('prediction-results').innerHTML = `<p>Error: ${error.message}</p>`;
    }
}

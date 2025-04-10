import React, { useEffect, useState } from 'react';

const CombinedData = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch('/api/fetch/combined');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const result = await response.json();
                setData(result);
            } catch (error) {
                setError(error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;

    return (
        <div>
            <h2>Combined Data</h2>
            <h3>Bitvavo Data:</h3>
            <pre>{JSON.stringify(data.bitvavo, null, 2)}</pre>
            <h3>Binance Data:</h3>
            <pre>{JSON.stringify(data.binance, null, 2)}</pre>
        </div>
    );
};

export default CombinedData;

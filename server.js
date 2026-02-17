
import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import Amadeus from 'amadeus';

dotenv.config();

const app = express();
const port = 3001;

app.use(cors());
app.use(express.json());

const amadeus = new Amadeus({
    clientId: process.env.VITE_AMADEUS_CLIENT_ID,
    clientSecret: process.env.VITE_AMADEUS_CLIENT_SECRET
});

app.get('/api/search-flights', async (req, res) => {
    try {
        const { origin, destination, departureDate, returnDate, adults } = req.query;
        if (!origin || !destination || !departureDate) {
            return res.status(400).json({ error: 'Missing required parameters' });
        }

        const response = await amadeus.shopping.flightOffersSearch.get({
            originLocationCode: origin,
            destinationLocationCode: destination,
            departureDate: departureDate,
            returnDate: returnDate,
            adults: adults || '1',
            max: '10'
        });

        res.json(response.data);
    } catch (error) {
        console.error("Amadeus API Error:", error);
        res.status(500).json({ error: 'Error fetching flights', details: error.message });
    }
});

app.get('/api/search-hotels', async (req, res) => {
    try {
        const { cityCode } = req.query;
        if (!cityCode) {
            return res.status(400).json({ error: 'Missing cityCode' });
        }

        // 1. Get hotels in city
        const response = await amadeus.referenceData.locations.hotels.byCity.get({
            cityCode: cityCode
        });

        res.json(response.data);
    } catch (error) {
        console.error("Amadeus API Error:", error);
        res.status(500).json({ error: 'Error fetching hotels', details: error.message });
    }
});

app.listen(port, () => {
    console.log(`Backend server running on http://localhost:${port}`);
});

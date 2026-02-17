
// MOCK DATA FOR DEMO MODE
const MOCK_FLIGHTS = [
    {
        id: '1',
        itineraries: [{
            duration: 'PT2H30M',
            segments: [{
                carrierCode: 'AF',
                number: '1234',
                departure: { at: '2026-06-15T10:00:00' },
                arrival: { at: '2026-06-15T12:30:00' }
            }]
        }],
        price: { total: '150.00', currency: 'EUR' }
    },
    {
        id: '2',
        itineraries: [{
            duration: 'PT8H15M',
            segments: [{
                carrierCode: 'BA',
                number: '5678',
                departure: { at: '2026-06-15T14:45:00' },
                arrival: { at: '2026-06-15T23:00:00' }
            }]
        }],
        price: { total: '420.50', currency: 'EUR' }
    },
    {
        id: '3',
        itineraries: [{
            duration: 'PT1H15M',
            segments: [{
                carrierCode: 'LH',
                number: '9012',
                departure: { at: '2026-06-15T08:20:00' },
                arrival: { at: '2026-06-15T09:35:00' }
            }]
        }],
        price: { total: '95.99', currency: 'EUR' }
    }
];

const MOCK_HOTELS = [
    {
        hotelId: 'H1',
        name: 'Grand Hotel Paris',
        address: { cityName: 'Paris', countryCode: 'FR' },
        rating: 5
    },
    {
        hotelId: 'H2',
        name: 'Hilton London Metropole',
        address: { cityName: 'London', countryCode: 'GB' },
        rating: 4
    },
    {
        hotelId: 'H3',
        name: 'Riad Marrakech Center',
        address: { cityName: 'Marrakech', countryCode: 'MA' },
        rating: 4
    }
];

const API_URL = 'http://localhost:3001/api';
// TOGGLE DEMO MODE HERE
const DEMO_MODE = true;

export const searchFlights = async (params) => {
    if (DEMO_MODE) {
        console.log("DEMO MODE: Returning mock flights", params);
        return new Promise(resolve => setTimeout(() => resolve(MOCK_FLIGHTS), 800)); // Simulate API delay
    }

    try {
        const query = new URLSearchParams(params).toString();
        const response = await fetch(`${API_URL}/search-flights?${query}`);
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }
        return await response.json();
    } catch (error) {
        console.error("Flight Search Error:", error);
        throw error;
    }
};

export const searchHotels = async (params) => {
    if (DEMO_MODE) {
        console.log("DEMO MODE: Returning mock hotels", params);
        // Filter faux mock par ville si possible, sinon retour tout
        return new Promise(resolve => setTimeout(() => resolve(MOCK_HOTELS), 800));
    }

    try {
        const query = new URLSearchParams(params).toString();
        const response = await fetch(`${API_URL}/search-hotels?${query}`);
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }
        return await response.json();
    } catch (error) {
        console.error("Hotel Search Error:", error);
        throw error;
    }
};

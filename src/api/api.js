
const API_URL = 'http://localhost:3001/api';

export const searchFlights = async (params) => {
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

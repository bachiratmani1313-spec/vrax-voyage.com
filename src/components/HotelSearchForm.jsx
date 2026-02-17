
import React, { useState } from 'react';
import { Search, Loader2 } from 'lucide-react';
import { searchHotels } from '../api/api';

export default function HotelSearchForm() {
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState([]);
    const [params, setParams] = useState({
        cityCode: 'PAR', // Default to Paris for demo
    });

    const handleChange = (e) => {
        setParams({ ...params, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const data = await searchHotels(params);
            console.log("Hotel API Response:", data);
            setResults(Array.isArray(data) ? data : (data.data || []));
        } catch (err) {
            alert("Erreur lors de la recherche (vérifiez le backend ou les clés API)");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="search-section">
            <form className="search-form" onSubmit={handleSubmit}>
                <div className="form-group" style={{ gridColumn: 'span 2' }}>
                    <label>Ville (Code IATA)</label>
                    <input name="cityCode" value={params.cityCode} onChange={handleChange} className="form-control" placeholder="ex: PAR, LON, NYC" required />
                </div>
                <div className="form-group">
                    <button type="submit" disabled={loading} className="btn-primary" style={{ marginTop: '24px' }}>
                        {loading ? <Loader2 className="animate-spin" /> : <><Search size={18} /> Trouver un Hôtel</>}
                    </button>
                </div>
            </form>

            {results.length > 0 && (
                <div className="results-list">
                    <h3>Hôtels trouvés ({results.length})</h3>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '20px' }}>
                        {results.map((hotel, idx) => (
                            <div key={idx} className="flight-card" style={{ display: 'block' }}>
                                <h4 style={{ marginBottom: '5px', color: 'var(--primary)' }}>{hotel.name}</h4>
                                <p style={{ fontSize: '0.9rem', color: '#666' }}>ID: {hotel.hotelId}</p>
                                {hotel.address && (
                                    <p style={{ fontSize: '0.85rem' }}>{hotel.address.cityName}, {hotel.address.countryCode}</p>
                                )}
                                {/* Amadeus Hotel Search API might not return price in basic lookup without specific dates/guests, adapting display */}
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}

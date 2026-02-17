
import React, { useState } from 'react';
import { Search, Loader2 } from 'lucide-react';
import { searchFlights } from '../api/api';

export default function SearchForm() {
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState([]);
    const [params, setParams] = useState({
        origin: 'PAR',
        destination: 'LHR',
        departureDate: new Date().toISOString().split('T')[0],
        returnDate: '',
        adults: 1
    });

    const handleChange = (e) => {
        setParams({ ...params, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const data = await searchFlights(params);
            console.log("API Response:", data);
            setResults(Array.isArray(data) ? data : (data.data || []));
        } catch (err) {
            alert("Erreur lors de la recherche (vérifiez le backend)");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="search-section">
            <form className="search-form" onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>Départ (Code IATA)</label>
                    <input name="origin" value={params.origin} onChange={handleChange} className="form-control" placeholder="ex: PAR" required />
                </div>
                <div className="form-group">
                    <label>Arrivée (Code IATA)</label>
                    <input name="destination" value={params.destination} onChange={handleChange} className="form-control" placeholder="ex: NYC" required />
                </div>
                <div className="form-group">
                    <label>Date Aller</label>
                    <input type="date" name="departureDate" value={params.departureDate} onChange={handleChange} className="form-control" required />
                </div>
                <div className="form-group">
                    <button type="submit" disabled={loading} className="btn-primary" style={{ marginTop: '24px' }}>
                        {loading ? <Loader2 className="animate-spin" /> : <><Search size={18} /> Rechercher</>}
                    </button>
                </div>
            </form>

            {results.length > 0 && (
                <div className="results-list">
                    <h3>Résultats ({results.length})</h3>
                    {results.map((flight, idx) => (
                        <div key={idx} className="flight-card">
                            <div className="flight-info">
                                <h4>{flight.itineraries[0].segments[0].carrierCode} - {flight.itineraries[0].segments[0].number}</h4>
                                <p>{flight.itineraries[0].duration.replace('PT', '').toLowerCase()}</p>
                            </div>
                            <div className="flight-price">
                                {flight.price.total} {flight.price.currency}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}


import React from 'react';

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import SearchForm from './components/SearchForm';
import HotelSearchForm from './components/HotelSearchForm';
import { MentionsLegales, PolitiqueConfidentialite } from './pages/Legal';
import { Briefcase, Plane, Hotel } from 'lucide-react';
import './index.css';

function Home() {
  return (
    <>
      <Navbar />
      <div className="hero">
        <h1>Comparez les meilleurs tarifs de voyage</h1>
        <p>Vrax-Voyage est votre comparateur universel. Accédez instantanément aux offres de centaines d'agences en un clic.</p>
      </div>

      <main className="container">
        {/* SECTION VOLS */}
        <h2 id="vols" className="section-title"><Plane className="mr-2" /> Recherche de Vols</h2>
        <section className="widget-container">
          <SearchForm />
        </section>

        {/* SECTION HÔTELS */}
        <h2 id="hotels" className="section-title"><Hotel className="mr-2" /> Réservation d'Hôtels</h2>
        <section className="widget-container">
          <HotelSearchForm />
        </section>

        {/* A PROPOS */}
        <h2 id="a-propos" className="section-title"><Briefcase className="mr-2" /> Qui sommes-nous ?</h2>
        <section className="about-box">
          <p>
            <strong>Vrax-Voyage.com</strong> est une plateforme de comparaison de voyages indépendante.
            Notre mission est d'aider les voyageurs à trouver les meilleures offres sur le marché en centralisant
            les recherches des plus grandes agences mondiales (Compagnies aériennes, Chaînes hôtelières, Loueurs).
          </p>
          <p style={{ marginTop: '15px' }}>
            Nous ne vendons pas de voyages directement, mais nous redirigeons nos utilisateurs vers les sites
            de réservation officiels. Ce service est gratuit pour l'utilisateur.
          </p>
        </section>

        {/* INSPIRATION */}
        <h2 className="section-title">Destinations Populaires</h2>
        <div className="inspiration-grid">
          {['Paris', 'Bali', 'New York', 'Marrakech'].map((city) => (
            <div className="inspire-card" key={city}>
              <img src={`https://picsum.photos/seed/${city}/400/300`} alt={city} />
              <div className="inspire-text">{city}</div>
            </div>
          ))}
        </div>
      </main>

      <footer>
        <div className="footer-content">
          <div className="footer-col">
            <h4>Vrax-Voyage.com</h4>
            <p>Votre comparateur de confiance pour des économies sur vos voyages.</p>
          </div>
          <div className="footer-col">
            <h4>Liens Utiles</h4>
            <ul>
              <li><a href="/">Accueil</a></li>
              <li><a href="/mentions-legales">Mentions Légales</a></li>
              <li><a href="/politique-confidentialite">Politique de Confidentialité</a></li>
              <li><a href="mailto:contact@vrax-voyage.com">Contact</a></li>
            </ul>
          </div>
          <div className="footer-col">
            <h4>Nos Partenaires</h4>
            <ul>
              <li><a href="#">Skyscanner</a></li>
              <li><a href="#">Booking.com</a></li>
              <li><a href="#">Expedia</a></li>
            </ul>
          </div>
        </div>
        <div className="legal-line">
          &copy; 2026 Vrax-Voyage.com. Tous droits réservés.
        </div>
      </footer>
    </>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/mentions-legales" element={<MentionsLegales />} />
        <Route path="/politique-confidentialite" element={<PolitiqueConfidentialite />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;



import React from 'react';
import Navbar from '../components/Navbar';
import './Legal.css';

export const MentionsLegales = () => (
    <div className="legal-page">
        <Navbar />
        <div className="container" style={{ marginTop: '50px' }}>
            <h1>Mentions Légales</h1>
            <section>
                <h2>1. Éditeur du site</h2>
                <p><strong>Vrax-Voyage.com</strong></p>
                <p>Email : contact@vrax-voyage.com</p>
                <p>Hébergeur : [Nom de votre hébergeur]</p>
            </section>

            <section>
                <h2>2. Propriété intellectuelle</h2>
                <p>Tous les contenus présents, tels que les textes, graphiques, logos, images, photographies, vidéos présents sur ce site sont, sauf mention contraire, la propriété de Vrax-Voyage.</p>
            </section>

            <section>
                <h2>3. Responsabilité</h2>
                <p>Les informations fournies sur ce site le sont à titre informatif. Vrax-Voyage ne saurait garantir l'exactitude, la complétude, l'actualité des informations diffusées sur le site.</p>
            </section>
        </div>
    </div>
);

export const PolitiqueConfidentialite = () => (
    <div className="legal-page">
        <Navbar />
        <div className="container" style={{ marginTop: '50px' }}>
            <h1>Politique de Confidentialité</h1>
            <p>Dernière mise à jour : 17 Février 2026</p>

            <section>
                <h2>1. Collecte des données</h2>
                <p>Nous ne collectons aucune donnée personnelle sensible lors de votre recherche de vol. Les données saisies servent uniquement à interroger les API de nos partenaires.</p>
            </section>

            <section>
                <h2>2. Cookies</h2>
                <p>Ce site utilise des cookies pour améliorer l'expérience utilisateur et réaliser des statistiques de visites anonymes.</p>
            </section>

            <section>
                <h2>3. Liens d'affiliation</h2>
                <p>Notre site contient des liens d'affiliation. Lorsque vous cliquez sur ces liens, nous pouvons percevoir une commission. Cela n'impacte pas le prix que vous payez.</p>
            </section>
        </div>
    </div>
);

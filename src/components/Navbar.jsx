
import React from 'react';
import { Plane, Hotel, Info, Home } from 'lucide-react';

export default function Navbar() {
    const scrollTo = (id) => {
        if (!id) window.scrollTo({ top: 0, behavior: 'smooth' });
        else document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
    };

    return (
        <header>
            <div className="container nav-flex">
                <a className="logo" onClick={() => scrollTo()}>Vrax-<span>Voyage.com</span></a>
                <nav className="nav-menu">
                    <a onClick={() => scrollTo()}><Home size={16} /> Accueil</a>
                    <a onClick={() => scrollTo('vols')}><Plane size={16} /> Vols</a>
                    <a onClick={() => scrollTo('hotels')}><Hotel size={16} /> Hôtels</a>
                    <a onClick={() => scrollTo('a-propos')}><Info size={16} /> À propos</a>
                </nav>
            </div>
        </header>
    );
}

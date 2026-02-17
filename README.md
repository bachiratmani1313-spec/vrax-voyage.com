
# Vrax-Voyage Reborn

Application de comparaison de vols et d'hôtels utilisant l'API Amadeus.

## Prérequis

1.  **Clés API Amadeus** :
    *   Créez un compte sur [Amadeus for Developers](https://developers.amadeus.com/).
    *   Créez une nouvelle application pour obtenir votre `API Key` et `API Secret`.
    *   Copiez ces clés dans le fichier `.env` à la racine du projet :
        ```env
        VITE_AMADEUS_CLIENT_ID=votre_cle_api
        VITE_AMADEUS_CLIENT_SECRET=votre_secret_api
        ```

## Installation

```bash
npm install
```

## Lancement

Vous devez lancer deux terminaux séparés :

**Terminal 1 (Backend - Serveur API) :**
```bash
npm run server
```

**Terminal 2 (Frontend - Site Web) :**
```bash
npm run dev
```

Ensuite, ouvrez votre navigateur sur le lien indiqué (généralement `http://localhost:5173`).

## Fonctionnalités

*   Recherche de vols en temps réel via Amadeus.
*   Interface responsive et moderne.
*   Structure prête pour l'ajout de la recherche d'hôtels.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Récupère les vols les moins chers pour les routes de Vrax Voyage via l'API
Travelpayouts (Data API) et écrit deals.json à la racine du site.
Le token vient du secret GitHub TRAVELPAYOUTS_TOKEN — jamais exposé au public.
"""
import os, json, datetime, urllib.parse, urllib.request

TOKEN  = os.environ.get("TRAVELPAYOUTS_TOKEN", "")
MARKER = os.environ.get("TP_MARKER", "704469")   # identifiant partenaire (paie Bachir)
CURRENCY = "eur"

# (origine, destination, ville).  Priorité : Belgique ↔ Maghreb, Charleroi ↔ Algérie.
ROUTES = [
    ("BRU", "RAK", "Marrakech"), ("BRU", "CMN", "Casablanca"), ("BRU", "NDR", "Nador"),
    ("BRU", "TNG", "Tanger"),    ("BRU", "FEZ", "Fès"),        ("BRU", "OUD", "Oujda"),
    ("BRU", "AGA", "Agadir"),    ("BRU", "RBA", "Rabat"),
    ("BRU", "ALG", "Alger"),     ("BRU", "ORN", "Oran"),       ("BRU", "TUN", "Tunis"),
    ("BRU", "DJE", "Djerba"),
    # Charleroi (forte communauté algérienne — priorité)
    ("CRL", "ALG", "Alger"),     ("CRL", "CZL", "Constantine"),("CRL", "ORN", "Oran"),
    ("CRL", "BJA", "Béjaïa"),    ("CRL", "NDR", "Nador"),      ("CRL", "TNG", "Tanger"),
    ("CRL", "FEZ", "Fès"),       ("CRL", "OUD", "Oujda"),      ("CRL", "RAK", "Marrakech"),
]

MOIS = ["", "Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Aoû", "Sep", "Oct", "Nov", "Déc"]


def cheapest(origin, dest):
    q = urllib.parse.urlencode({
        "origin": origin, "destination": dest, "currency": CURRENCY,
        "sorting": "price", "direct": "false", "limit": 1,
        "one_way": "false", "token": TOKEN,
    })
    url = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates?" + q
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=25) as r:
            j = json.load(r)
        data = j.get("data") or []
        return data[0] if data else None
    except Exception as e:
        print("  ⚠️", origin, dest, "→", e)
        return None


def aviasales_link(item, o, d):
    link = item.get("link") or ""
    url = ("https://www.aviasales.com" + link) if link else \
          ("https://www.aviasales.com/search/" + o + d)
    url += ("&" if "?" in url else "?") + "marker=" + MARKER
    return url


def mois_label(iso):
    try:
        return MOIS[int(iso[5:7])] + " · A/R"
    except Exception:
        return "A/R"


def main():
    if not TOKEN:
        print("❌ TRAVELPAYOUTS_TOKEN manquant.")
        return
    deals = []
    for o, d, ville in ROUTES:
        item = cheapest(o, d)
        if not item:
            continue
        try:
            price = round(float(item.get("price", 0)))
        except Exception:
            price = 0
        if price <= 0:
            continue
        deals.append({
            "o": o, "d": d, "city": ville, "price": price,
            "depart": (item.get("departure_at") or "")[:10],
            "ret": (item.get("return_at") or "")[:10],
            "when": mois_label(item.get("departure_at") or ""),
            "link": aviasales_link(item, o, d),
        })
        print(f"  ✓ {o}→{d} : {price}€")

    # un seul vol par destination (le moins cher) → variété, pas de doublons
    best = {}
    for x in deals:
        if x["d"] not in best or x["price"] < best[x["d"]]["price"]:
            best[x["d"]] = x
    deals = sorted(best.values(), key=lambda x: x["price"])[:12]

    out = {"updated": datetime.date.today().isoformat(), "deals": deals}
    with open("deals.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"✅ {len(deals)} bons plans écrits dans deals.json")


if __name__ == "__main__":
    main()

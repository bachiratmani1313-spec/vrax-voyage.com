#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vrax Voyage — moteur de bons plans.

1) Cible les PROCHAINS mois réels de voyage (fini le "tout septembre").
2) Garde un historique des prix (price_history.json) et détecte les PROMOS :
   un prix qui chute nettement sous sa moyenne récente est marqué promo=true
   et remonte en tête. C'est l'avantage de Vrax sur les comparateurs.

Token : secret GitHub TRAVELPAYOUTS_TOKEN — jamais exposé au public.
"""
import os, json, time, datetime, statistics, urllib.parse, urllib.request

TOKEN    = os.environ.get("TRAVELPAYOUTS_TOKEN", "")
MARKER   = os.environ.get("TP_MARKER", "704469")   # identifiant partenaire (paie Bachir)
CURRENCY = "eur"

# --- Réglages que Bachir peut ajuster facilement ---
WINDOW_MONTHS   = 4      # nb de mois interrogés à partir d'aujourd'hui
ACTIVE_WINDOW   = 2      # mois "imminents" affichés en priorité (relevance)
PROMO_DROP      = 0.20   # baisse mini pour qu'un prix devienne une PROMO (20%)
PROMO_MIN_HIST  = 4      # nb mini de relevés avant de pouvoir crier "promo"
HIST_MAX        = 40     # longueur max de l'historique par route+mois
MAX_DEALS       = 12     # nb de cartes affichées sur le site
HIST_FILE       = "price_history.json"

# (origine, destination, ville). Priorité : Belgique <-> Maghreb, Charleroi <-> Algérie.
ROUTES = [
    ("BRU", "RAK", "Marrakech"), ("BRU", "CMN", "Casablanca"), ("BRU", "NDR", "Nador"),
    ("BRU", "TNG", "Tanger"),    ("BRU", "FEZ", "Fès"),        ("BRU", "OUD", "Oujda"),
    ("BRU", "AGA", "Agadir"),    ("BRU", "RBA", "Rabat"),
    ("BRU", "ALG", "Alger"),     ("BRU", "ORN", "Oran"),       ("BRU", "TUN", "Tunis"),
    ("BRU", "DJE", "Djerba"),
    ("CRL", "ALG", "Alger"),     ("CRL", "CZL", "Constantine"),("CRL", "ORN", "Oran"),
    ("CRL", "BJA", "Béjaïa"),    ("CRL", "NDR", "Nador"),      ("CRL", "TNG", "Tanger"),
    ("CRL", "FEZ", "Fès"),       ("CRL", "OUD", "Oujda"),      ("CRL", "RAK", "Marrakech"),
]
_FR_ORIGINS = ["CDG", "ORY", "LYS", "MRS", "TLS", "LIL"]   # Paris, Lyon, Marseille, Toulouse, Lille
_MAGHREB = [
    ("RAK", "Marrakech"), ("CMN", "Casablanca"), ("NDR", "Nador"), ("TNG", "Tanger"),
    ("FEZ", "Fès"), ("OUD", "Oujda"), ("AGA", "Agadir"), ("ALG", "Alger"),
    ("ORN", "Oran"), ("CZL", "Constantine"), ("TUN", "Tunis"), ("DJE", "Djerba"),
]
for _o in _FR_ORIGINS:
    for _d, _city in _MAGHREB:
        ROUTES.append((_o, _d, _city))

MOIS = ["", "Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Aoû", "Sep", "Oct", "Nov", "Déc"]


def target_months():
    """Renvoie les prochains mois 'YYYY-MM' à partir d'aujourd'hui."""
    today = datetime.date.today()
    out, y, m = [], today.year, today.month
    for _ in range(WINDOW_MONTHS):
        out.append(f"{y:04d}-{m:02d}")
        m += 1
        if m > 12:
            m, y = 1, y + 1
    return out


def cheapest(origin, dest, month):
    """Vol A/R le moins cher pour un mois donné (departure_at = YYYY-MM)."""
    q = urllib.parse.urlencode({
        "origin": origin, "destination": dest, "currency": CURRENCY,
        "departure_at": month, "sorting": "price", "direct": "false",
        "limit": 1, "one_way": "false", "token": TOKEN,
    })
    url = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates?" + q
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=25) as r:
            j = json.load(r)
        data = j.get("data") or []
        return data[0] if data else None
    except Exception as e:
        print("  ⚠️", origin, dest, month, "→", e)
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


def load_history():
    try:
        with open(HIST_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def main():
    if not TOKEN:
        print("❌ TRAVELPAYOUTS_TOKEN manquant.")
        return

    months = target_months()
    active = set(months[:ACTIVE_WINDOW])      # mois imminents (affichés en priorité)
    today_iso = datetime.date.today().isoformat()
    history = load_history()
    candidates = []

    for o, d, ville in ROUTES:
        for month in months:
            item = cheapest(o, d, month)
            time.sleep(0.25)                  # on reste poli avec l'API
            if not item:
                continue
            try:
                price = round(float(item.get("price", 0)))
            except Exception:
                price = 0
            if price <= 0:
                continue

            key = f"{o}-{d}-{month}"
            hist = history.get(key, [])
            past = [h["p"] for h in hist][-14:]     # 14 derniers relevés

            promo, baseline, discount = False, None, 0
            if len(past) >= PROMO_MIN_HIST:
                baseline = round(statistics.median(past))
                if baseline > 0 and price <= baseline * (1 - PROMO_DROP):
                    promo = True
                    discount = round((baseline - price) / baseline * 100)

            # on enregistre le relevé du jour (1 par route+mois/jour)
            if not hist or hist[-1].get("date") != today_iso:
                hist.append({"date": today_iso, "p": price})
            else:
                hist[-1]["p"] = min(hist[-1]["p"], price)
            history[key] = hist[-HIST_MAX:]

            candidates.append({
                "o": o, "d": d, "city": ville, "price": price,
                "depart": (item.get("departure_at") or "")[:10],
                "ret": (item.get("return_at") or "")[:10],
                "when": mois_label(item.get("departure_at") or ""),
                "link": aviasales_link(item, o, d),
                "month": month, "active": month in active,
                "promo": promo, "baseline": baseline, "discount": discount,
            })
            tag = f" 🔥-{discount}%" if promo else ""
            print(f"  ✓ {o}→{d} {month} : {price}€{tag}")

    # 1) toutes les PROMOS (n'importe quel mois) — c'est notre force
    promos = [c for c in candidates if c["promo"]]
    # 2) sinon, le moins cher par destination dans la fenêtre imminente
    normal = [c for c in candidates if not c["promo"] and c["active"]]
    # repli : si aucune date imminente n'a renvoyé de prix, on prend le reste
    if not normal:
        normal = [c for c in candidates if not c["promo"]]

    best = {}
    for x in sorted(normal, key=lambda c: c["price"]):
        if x["d"] not in best:
            best[x["d"]] = x

    promos_sorted = sorted(promos, key=lambda c: c["discount"], reverse=True)
    rest_sorted   = sorted(best.values(), key=lambda c: c["price"])

    seen, deals = set(), []
    for x in promos_sorted + rest_sorted:     # promos d'abord, puis les meilleurs prix
        sig = (x["o"], x["d"], x["month"])
        if sig in seen:
            continue
        seen.add(sig)
        deals.append(x)
        if len(deals) >= MAX_DEALS:
            break

    out = {"updated": today_iso, "deals": deals}
    with open("deals.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    with open(HIST_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

    n_promo = sum(1 for d in deals if d["promo"])
    print(f"✅ {len(deals)} bons plans écrits ({n_promo} promo) dans deals.json")
    print(f"🗂️  historique : {len(history)} routes/mois suivis")


if __name__ == "__main__":
    main()

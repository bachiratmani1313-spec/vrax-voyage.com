#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vrax Voyage — Paires Été (l'idée phare de Bachir).

Principe : au lieu d'un billet A/R classique, on combine DEUX allers simples :
  ALLER  Europe → Maghreb  (mois M)
  RETOUR Maghreb → Europe  (mois M+1, soit ~1 mois plus tard)
C'est souvent moins cher, et surtout ça colle au vrai rythme des familles
de la diaspora (départ juillet/août, retour août/septembre/octobre).

Sortie : pairs.json, groupé par communauté (Maroc / Algérie / Tunisie).
Script totalement séparé de update_deals.py — ne touche pas au robot existant.

Token : secret GitHub TRAVELPAYOUTS_TOKEN — jamais exposé au public.
"""
import os, json, time, datetime, urllib.parse, urllib.request

TOKEN    = os.environ.get("TRAVELPAYOUTS_TOKEN", "")
MARKER   = os.environ.get("TP_MARKER", "704469")   # identifiant partenaire (paie Bachir)
CURRENCY = "eur"

# --- Réglages que Bachir peut ajuster facilement ---
SEASON_END   = "2026-10"   # dernier mois de RETOUR de la saison
MIN_GAP_DAYS = 14          # écart mini aller→retour (sinon paire incohérente)
MAX_GAP_DAYS = 55          # écart maxi aller→retour
MAX_PER_COMM = 8           # nb de paires affichées par communauté
OUT_FILE     = "pairs.json"

# Origines Europe (Belgique en tête — la maison)
ORIGINS = [
    ("BRU", "Bruxelles"), ("CRL", "Charleroi"),
    ("CDG", "Paris CDG"), ("ORY", "Paris Orly"),
    ("LYS", "Lyon"), ("MRS", "Marseille"), ("TLS", "Toulouse"), ("LIL", "Lille"),
]

# Destinations par communauté
COMMUNITIES = {
    "maroc": {
        "label": "Maroc", "flag": "🇲🇦",
        "dests": [("RAK", "Marrakech"), ("CMN", "Casablanca"), ("NDR", "Nador"),
                  ("TNG", "Tanger"), ("FEZ", "Fès"), ("OUD", "Oujda"),
                  ("AGA", "Agadir"), ("RBA", "Rabat")],
    },
    "algerie": {
        "label": "Algérie", "flag": "🇩🇿",
        "dests": [("ALG", "Alger"), ("ORN", "Oran"),
                  ("CZL", "Constantine"), ("BJA", "Béjaïa")],
    },
    "tunisie": {
        "label": "Tunisie", "flag": "🇹🇳",
        "dests": [("TUN", "Tunis"), ("DJE", "Djerba")],
    },
}

MOIS = ["", "janvier", "février", "mars", "avril", "mai", "juin",
        "juillet", "août", "septembre", "octobre", "novembre", "décembre"]


def month_add(iso_month, n=1):
    y, m = int(iso_month[:4]), int(iso_month[5:7])
    m += n
    while m > 12:
        m, y = m - 12, y + 1
    return f"{y:04d}-{m:02d}"


def aller_months():
    """Mois de départ de la saison : du mois courant jusqu'à SEASON_END - 1 mois."""
    today = datetime.date.today()
    cur = f"{today.year:04d}-{today.month:02d}"
    out = []
    while month_add(cur) <= SEASON_END:
        out.append(cur)
        cur = month_add(cur)
    return out


def cheapest_oneway(origin, dest, month):
    """Vol ALLER SIMPLE le moins cher pour un mois donné."""
    q = urllib.parse.urlencode({
        "origin": origin, "destination": dest, "currency": CURRENCY,
        "departure_at": month, "sorting": "price", "direct": "false",
        "limit": 1, "one_way": "true", "token": TOKEN,
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


def fr_date(iso):
    """'2026-08-28' → '28 août'"""
    try:
        return f"{int(iso[8:10])} {MOIS[int(iso[5:7])]}"
    except Exception:
        return iso


def seg(item, o, d):
    try:
        price = round(float(item.get("price", 0)))
    except Exception:
        price = 0
    date = (item.get("departure_at") or "")[:10]
    return {"price": price, "date": date, "date_fr": fr_date(date),
            "link": aviasales_link(item, o, d)}


def main():
    if not TOKEN:
        print("❌ TRAVELPAYOUTS_TOKEN manquant.")
        return

    months = aller_months()
    today_iso = datetime.date.today().isoformat()
    cache_retour = {}   # (d, o, mois) → item : évite les appels en double
    result = {}

    for comm_key, comm in COMMUNITIES.items():
        pairs = []
        for d_code, d_city in comm["dests"]:
            for o_code, o_city in ORIGINS:
                for m in months:
                    aller = cheapest_oneway(o_code, d_code, m)
                    time.sleep(0.25)                # on reste poli avec l'API
                    if not aller:
                        continue
                    m_ret = month_add(m)
                    ck = (d_code, o_code, m_ret)
                    if ck not in cache_retour:
                        cache_retour[ck] = cheapest_oneway(d_code, o_code, m_ret)
                        time.sleep(0.25)
                    retour = cache_retour[ck]
                    if not retour:
                        continue

                    s_a, s_r = seg(aller, o_code, d_code), seg(retour, d_code, o_code)
                    if s_a["price"] <= 0 or s_r["price"] <= 0:
                        continue
                    try:
                        da = datetime.date.fromisoformat(s_a["date"])
                        dr = datetime.date.fromisoformat(s_r["date"])
                        gap = (dr - da).days
                    except Exception:
                        continue
                    if gap < MIN_GAP_DAYS or gap > MAX_GAP_DAYS:
                        continue

                    pairs.append({
                        "o": o_code, "o_city": o_city,
                        "d": d_code, "city": d_city,
                        "aller": s_a, "retour": s_r,
                        "total": s_a["price"] + s_r["price"],
                        "gap": gap, "month": m,
                    })
                    print(f"  ✓ {o_code}→{d_code} {m} : {s_a['price']}€ + {s_r['price']}€ = {s_a['price']+s_r['price']}€ ({gap} j)")

        # meilleure paire par (origine, destination), puis tri par prix total
        best = {}
        for p in sorted(pairs, key=lambda x: x["total"]):
            k = (p["o"], p["d"])
            if k not in best:
                best[k] = p
        top = sorted(best.values(), key=lambda x: x["total"])[:MAX_PER_COMM]
        if top:
            top[0]["hero"] = True               # coup de cœur de la communauté
        result[comm_key] = {"label": comm["label"], "flag": comm["flag"], "pairs": top}

    out = {"updated": today_iso, "season": "été 2026", "communities": result}
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    total = sum(len(v["pairs"]) for v in result.values())
    print(f"✅ {total} paires écrites dans {OUT_FILE}")


if __name__ == "__main__":
    main()

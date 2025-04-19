# etl/enrich/load_country_religion_sparql.py

import requests, time, logging
from sqlalchemy import text
from utils.db import get_engine

SPARQL_URL = "https://query.wikidata.org/sparql"
HEADERS = {"User-Agent": "MusicAtlas/1.0 (kr@example.com)"}
engine = get_engine()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("wikidata_religion")

Q_TEMPLATE = """
SELECT ?religionLabel WHERE {
  ?country wdt:P297 "%s"; wdt:P2596 ?religion.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
LIMIT 1
"""

def fetch_religion(iso2):
    q = Q_TEMPLATE % iso2
    try:
        r = requests.get(
            SPARQL_URL,
            params={"query": q, "format": "json"},
            headers=HEADERS,
            timeout=10,
        )
        r.raise_for_status()
        items = r.json()["results"]["bindings"]
        return items[0]["religionLabel"]["value"] if items else None
    except Exception as e:
        log.warning("⚠️ %s: %s", iso2, e)
        return None

with engine.connect() as conn:
    countries = [row.iso2 for row in conn.execute(text("SELECT iso2 FROM staging.country"))]

for iso2 in countries:
    rel = fetch_religion(iso2)
    if rel:
        with engine.begin() as conn:
            conn.execute(text("""
                UPDATE staging.country
                SET majority_religion = :rel
                WHERE iso2 = :iso
            """), {"rel": rel, "iso": iso2})
        log.info("✅ %s → %s", iso2, rel)
    else:
        log.info("🚫 %s → no data", iso2)
    time.sleep(1)  # Wikidata rate-limit: 1 req/sec

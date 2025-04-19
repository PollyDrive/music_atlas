import requests, time
from sqlalchemy import text
from utils.db import get_engine

engine = get_engine()
MED = "https://api.worldbank.org/v2/country/{}/indicator/SP.POP.MED?format=json"

for iso, in engine.execute(text("SELECT iso2 FROM staging.country")):
    try:
        val = next(x["value"] for x in requests.get(MED.format(iso)).json()[1] if x["date"]=="2022")
        if val:
            with engine.begin() as conn:
                conn.execute(text("""
                    UPDATE staging.country SET median_age_2022 = :val WHERE iso2 = :iso
                """), {"val": val, "iso": iso})
    except Exception: pass
    time.sleep(.2)
print("✅ Median age done")

import requests, pandas as pd, time
from sqlalchemy import text
from utils.db import get_engine

engine = get_engine()
REST_URL = "https://restcountries.com/v3.1/alpha/{}"

with engine.begin() as conn:
    isos = [r[0] for r in conn.execute(text("SELECT iso2 FROM staging.country"))]

for iso in isos:
    try:
        langs = requests.get(REST_URL.format(iso)).json()[0]["languages"].values()
        lang_str = ", ".join(langs)

        with engine.begin() as conn:
            conn.execute(text("""
                UPDATE staging.country SET languages = :langs WHERE iso2 = :iso
            """), {"langs": lang_str, "iso": iso})
        print(f"✅ {iso} languages done")
    except Exception as e:
        print(f"⚠️ {iso} languages skip: {e}")
    time.sleep(0.2)



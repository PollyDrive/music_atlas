"""
load_depression_2021.py
"""
import requests
from sqlalchemy import text
from utils.db import get_engine

API = "https://apps.who.int/gho/athena/api/GHO/GDO_q35.json"
YEARS = [2021, 2019, 2017]          # градиент отката
FILTER_BASE = "COUNTRY:*;SEX:BTSX"
TARGET_COL = "depression_rate_2021" # уже существует
TARGET_TABLE = "staging.country"

def fetch_facts(year):
    params = {"filter": f"{FILTER_BASE};YEAR:{year}", "profile": "simple", "page_size": 5000}
    r = requests.get(API, params=params, timeout=30)
    r.raise_for_status()
    return r.json().get("fact", [])

def main():
    facts = []
    used_year = None

    for y in YEARS:
        data = fetch_facts(y)
        if data:                     # нашли непустой набор
            facts = data
            used_year = y
            break

    if not facts:
        raise RuntimeError("WHO API вернул пустой набор даже для резервных годов")

    if used_year != 2021:
        print(f"[warn] свежих значений за 2021 нет, используем {used_year}; "
              "строки за 2021 останутся NULL")

    # фильтруем: оставляем только записи ровно за 2021
    facts_2021 = [f for f in facts if int(f["YEAR"]) == 2021]

    if not facts_2021:
        print("[info] нет фактов 2021 года – ничего не обновляем")
        return

    pairs = [(f["COUNTRY"], float(f["Numeric Value"])) for f in facts_2021]

    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(
            text(f"""
                UPDATE {TARGET_TABLE} AS c
                SET    {TARGET_COL} = v.val
                FROM  (VALUES :pairs) AS v(iso3, val)
                WHERE c.iso3 = v.iso3;
            """).bindparams(pairs=pairs)
        )

    print(f"✓ Обновили {len(pairs)} стран значением depression_rate_2021")

if __name__ == "__main__":
    main()

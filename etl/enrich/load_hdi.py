import pandas as pd
import requests, time
from sqlalchemy import text
from utils.db import get_engine

engine = get_engine()
HDR = "https://hdr.undp.org/sites/default/files/hdro_statistical_data.csv"
df = (
    pd.read_csv(HDR)
    .query("Indicator=='Human Development Index (HDI)' and Year==2022")
)

for _, row in df.iterrows():
    iso = row["ISO3"].strip()[:2]         # грубое сопоставление
    hdi = row["Value"]
    with engine.begin() as conn:
        conn.execute(text("""
            UPDATE staging.country SET hdi_2022 = :hdi WHERE iso2 = :iso
        """), {"hdi": hdi, "iso": iso})
print("✅ HDI done")

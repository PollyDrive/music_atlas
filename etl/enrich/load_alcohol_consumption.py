import pandas as pd
import requests, logging
from sqlalchemy import text
from utils.db import get_engine

log = logging.getLogger("alcohol")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

engine = get_engine()

# 1. Скачиваем CSV
url = "https://ourworldindata.org/grapher/total-alcohol-consumption-per-capita-litres-of-pure-alcohol.csv?v=1&csvType=full"
df = pd.read_csv(url, storage_options={'User-Agent': 'OWID data fetch/1.0'})

# 2. Переименуем колонки для удобства
df = df.rename(columns={
    "Code": "iso3",
    "Year": "year",
    "Total alcohol consumption per capita (liters of pure alcohol, projected estimates, 15+ years of age)": "alcohol"})

# 3. Фильтруем нужный год
df = df[(df["year"] == 2019) & df["iso3"].notna() & df["alcohol"].notna()]

updated = 0
skipped = 0

# 4. Обновление БД
for _, row in df.iterrows():
    iso = row["iso3"]
    score = row["alcohol"]

    with engine.begin() as conn:
        result = conn.execute(text("""
            UPDATE staging.country
            SET alcohol_per_capita_2019 = :score
            WHERE iso3 = :iso
        """), {"score": score, "iso": iso})

        if result.rowcount > 0:
            updated += 1
            log.info("✅ %s → %.2f", iso, score)
        else:
            skipped += 1
            log.warning("⚠️  %s не найден в базе", iso)

log.info("🎯 Алкоголь: %d обновлено, %d пропущено", updated, skipped)

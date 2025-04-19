import requests
import time
import logging
from sqlalchemy import text
from utils.db import get_engine

# Логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("suicide_rate")


engine = get_engine()
WB_URL = "https://api.worldbank.org/v2/country/{}/indicator/SH.STA.SUIC.P5?format=json"

updated = 0
skipped = 0

with engine.connect() as conn:
    result = conn.execute(text("SELECT iso2 FROM staging.country"))
    iso_list = [r[0] for r in result]

for iso in iso_list:
    try:
        r = requests.get(WB_URL.format(iso), timeout=10)
        r.raise_for_status()
        data = r.json()

        # Проверка на корректный формат
        if not isinstance(data, list) or len(data) < 2 or not data[1]:
            log.warning("⚠️  %s → пустой или некорректный ответ", iso)
            skipped += 1
            continue

        val = next((x["value"] for x in data[1] if x["date"] == "2021" and x["value"] is not None), None)

        if val is not None:
            with engine.begin() as conn:
                conn.execute(text("""
                    UPDATE staging.country
                    SET suicide_rate_2021 = :val
                    WHERE iso2 = :iso
                """), {"val": val, "iso": iso})
            log.info("✅ %s → %.2f", iso, val)
            updated += 1
        else:
            log.info("🚫 %s → нет данных за 2021", iso)
            skipped += 1

    except Exception as e:
        log.error("❌ Ошибка при обработке %s: %s", iso, e)
        skipped += 1

    time.sleep(0.3)

log.info("🎯 Завершено: обновлено %d, пропущено %d", updated, skipped)

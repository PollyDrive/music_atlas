import pandas as pd
from sqlalchemy import text
from utils.db import get_engine
import logging

# Логгинг
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("depression_rate")

engine = get_engine()
CSV_PATH = "data/IHME-GBD_2021_DATA.csv"


def main():
    # Чтение и предварительный вывод заголовков
    df = pd.read_csv(CSV_PATH)
    # df = pd.read_csv(CSV_PATH, dtype={"Score": float})
    log.info("📄 Загружено строк: %d", len(df))
    log.info("📊 Заголовки: %s", list(df.columns))

    updated = 0
    skipped = 0

    for _, row in df.iterrows():
        iso = row.get("ISO") or row.get("ISO 3") or row.get("iso2")
        val = row.get("val")

        if pd.notna(iso) and pd.notna(val):
            print(pd.notna(iso))
            with engine.begin() as conn:
                result = conn.execute(text("""
                    UPDATE staging.country
                    SET depression_rate_2021 = :val
                    WHERE iso2 = :iso
                """), {"val": val, "iso": iso})
                if result.rowcount > 0:
                    updated += 1
                    log.info("✅ %s → %.2f", iso, val)
                else:
                    skipped += 1
                    log.warning("⚠️  %s не найден в базе", iso)
        else:
            skipped += 1
            log.warning("⛔️ Пропущена строка: iso=%s, val=%s", iso, val)

    log.info("🎯 Обновлено: %d | Пропущено: %d", updated, skipped)
if __name__ == "__main__":
    main()

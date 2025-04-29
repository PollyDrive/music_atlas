import pandas as pd
from sqlalchemy import text
from utils.db import get_engine
import logging

# Логгинг
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("press_freedom")
engine = get_engine()
# https://rsf.org/en/index?year=2024
CSV_PATH = "data/RSF_2024_Data.csv"

def main():
    # Чтение и предварительный вывод заголовков
    df = pd.read_csv(CSV_PATH, sep=";", decimal=",")
    # df = pd.read_csv(CSV_PATH, dtype={"Score": float})
    log.info("📄 Загружено строк: %d", len(df))
    log.info("📊 Заголовки: %s", list(df.columns))

    updated = 0
    skipped = 0

    for _, row in df.iterrows():
        iso = row.get("ISO") or row.get("ISO 3") or row.get("iso3")
        score = row.get("Score") or row.get("Global Score")

        if pd.notna(iso) and pd.notna(score):
            print(pd.notna(iso))
            with engine.begin() as conn:
                result = conn.execute(text("""
                    UPDATE staging.country
                    SET press_freedom_2024 = :score
                    WHERE iso3 = :iso
                """), {"score": score, "iso": iso})
                if result.rowcount > 0:
                    updated += 1
                    log.info("✅ %s → %.2f", iso, score)
                else:
                    skipped += 1
                    log.warning("⚠️  %s не найден в базе", iso)
        else:
            skipped += 1
            log.warning("⛔️ Пропущена строка: iso=%s, score=%s", iso, score)

    log.info("🎯 Обновлено: %d | Пропущено: %d", updated, skipped)

if __name__ == "__main__":
    main()

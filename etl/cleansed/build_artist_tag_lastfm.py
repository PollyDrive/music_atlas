import pandas as pd
from sqlalchemy import text
from datetime import date
from utils.db import get_engine

# Настройки
engine = get_engine()
SCHEMA_SOURCE = "staging"
TABLE_SOURCE = "artist"
SCHEMA_TARGET = "cleansed"
TABLE_TARGET = "artist_tag"
SOURCE_LABEL = "lastfm"
FETCH_DATE = date.today()

def main():
    # Создаём таблицу для связки артистов и тегов (если не существует)
    with engine.begin() as conn:
        conn.execute(text(f"""
            CREATE SCHEMA IF NOT EXISTS cleansed;

            CREATE TABLE IF NOT EXISTS {SCHEMA_TARGET}.{TABLE_TARGET} (
                artist_id INT REFERENCES {SCHEMA_SOURCE}.artist(artist_id),
                name TEXT,
                tag TEXT,
                source TEXT,
                fetch_date DATE,
                PRIMARY KEY (artist_id, tag)
            );
        """))

    # Загружаем артистов и их теги
    with engine.connect() as conn:
        result = conn.execute(text(f"""
            SELECT artist_id, name, tags
            FROM {SCHEMA_SOURCE}.{TABLE_SOURCE}
            WHERE tags IS NOT NULL AND tags != ''
        """))
        rows = result.fetchall()

    print(f"🔍 Артистов с тегами: {len(rows)}")
    inserted = 0

    # Парсим строки тегов и вставляем по одному тегу
    for artist_id, name, tag_string in rows:
        tags = [t.strip() for t in tag_string.split(",") if t.strip()]
        for tag in tags:
            try:
                with engine.begin() as conn:
                    conn.execute(text(f"""
                        INSERT INTO {SCHEMA_TARGET}.{TABLE_TARGET} (artist_id, name, tag, source, fetch_date)
                        VALUES (:artist_id, :name, :tag, :source, :fetch_date)
                        ON CONFLICT DO NOTHING
                    """), {
                        "artist_id": artist_id,
                        "name": name,
                        "tag": tag,
                        "source": SOURCE_LABEL,
                        "fetch_date": FETCH_DATE
                    })
                inserted += 1
            except Exception as e:
                print(f"❌ Ошибка вставки для {name} / {tag}: {e}")

    print(f"🎉 Всего вставлено пар artist-tag: {inserted}")


if __name__ == "__main__":
    main()
from sqlalchemy import text
from utils.db import get_engine

engine = get_engine()
SCHEMA = "staging"

# Поддерживаемые формы невалидных имён
INVALID_NAMES = ("[unknown]", "unknown", "unknown artist")

with engine.connect() as conn:
    # Получаем артистов с плохими именами и валидным alias
    result = conn.execute(text(f"""
        SELECT artist_id, name, alias
        FROM {SCHEMA}.artist
        WHERE LOWER(name) IN :invalid_names
          AND alias IS NOT NULL
          AND alias <> '';
    """), {"invalid_names": INVALID_NAMES})
    
    to_fix = result.fetchall()

print(f"🔍 Найдено для исправления: {len(to_fix)} артистов")

for artist_id, name, alias in to_fix:
    try:
        with engine.begin() as conn:
            # Обновляем artist.name
            conn.execute(text(f"""
                UPDATE {SCHEMA}.artist
                SET name = :alias
                WHERE artist_id = :artist_id
            """), {"alias": alias, "artist_id": artist_id})

            # Обновляем имя в country_top_artists
            conn.execute(text(f"""
                UPDATE {SCHEMA}.country_top_artists
                SET artist_name = :alias
                WHERE artist_name = :old_name
            """), {"alias": alias, "old_name": name})

        print(f"✅ Исправлено: {name} → {alias}")

    except Exception as e:
        print(f"❌ Ошибка при обновлении {name}: {e}")

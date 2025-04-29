import os
import requests
import time
from sqlalchemy import text
from utils.db import get_engine

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
LASTFM_API_URL = os.getenv("LASTFM_API_URL")
engine = get_engine()

def main():
    with engine.connect() as conn:
        artists = conn.execute(text("""
            SELECT artist_id, name
            FROM staging.artist
            WHERE (tags IS NULL OR tags = '') AND name IS NOT NULL
        """)).fetchall()

    for artist_id, name in artists:
        try:
            params = {
                "method": "artist.getinfo",
                "artist": name,
                "api_key": LASTFM_API_KEY,
                "format": "json"
            }
            response = requests.get(LASTFM_API_URL, params=params)
            if response.status_code != 200:
                print(f"⚠️ Ошибка {response.status_code} при запросе: {name}")
                continue

            tags = response.json().get("artist", {}).get("tags", {}).get("tag", [])
            tag_list = ", ".join(tag["name"] for tag in tags) if tags else None

            if tag_list:
                with engine.begin() as conn:
                    conn.execute(text("""
                        UPDATE staging.artist
                        SET tags = :tags
                        WHERE artist_id = :artist_id
                    """), {"tags": tag_list, "artist_id": artist_id})
                print(f"✅ Теги обновлены для {name}")
            else:
                print(f"ℹ️ Теги не найдены для {name}")

            time.sleep(1)

        except Exception as e:
            print(f"❌ Ошибка при обработке {name}: {e}")
if __name__ == "__main__":
    main()
import os
import requests
from sqlalchemy import text
from utils.db import get_engine
from utils.logger import get_logger
from time import sleep

# ─── Инициализация ──────────────────────────────────────────────
engine = get_engine()
logger = get_logger("artist_info_loader", "logs/load_artist_info.log")

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
API_URL = os.getenv("LASTFM_API_URL")

# ─── Получение инфы по артисту ──────────────────────────────────
def fetch_artist_info(artist_name):
    try:
        params = {
            "method": "artist.getInfo",
            "artist": artist_name,
            "api_key": LASTFM_API_KEY,
            "format": "json"
        }
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.warning(f"⛔ Ошибка запроса к API для артиста '{artist_name}': {e}")
        return None

# ─── Основной процесс ───────────────────────────────────────────
def main():
    with engine.begin() as conn:
        artists = conn.execute(text("SELECT artist_id, name FROM staging.artist WHERE name IS NOT NULL")).fetchall()
        logger.info(f"🔍 Найдено исполнителей: {len(artists)}")

        for artist_id, name in artists:
            logger.info(f"📡 Обработка: {name}")

            try:
                data = fetch_artist_info(name)
                if not data or 'artist' not in data:
                    logger.warning(f"⚠️ Нет данных для: {name}")
                    continue

                artist_data = data['artist']
                summary = artist_data.get('bio', {}).get('summary')
                listeners = artist_data.get('stats', {}).get('listeners')
                playcount = artist_data.get('stats', {}).get('playcount')
                tags = ', '.join([tag['name'] for tag in artist_data.get('tags', {}).get('tag', [])])
                url = artist_data.get('url')

                conn.execute(text("""
                    UPDATE staging.artist
                    SET
                        bio_summary = :summary,
                        listeners = :listeners,
                        playcount = :playcount,
                        tags = :tags,
                        url = :url
                    WHERE artist_id = :artist_id
                """), {
                    "summary": summary,
                    "listeners": listeners,
                    "playcount": playcount,
                    "tags": tags,
                    "url": url,
                    "artist_id": artist_id
                })

                logger.info(f"✅ Обновлено: {name}")

            except Exception as e:
                logger.error(f"🔥 Ошибка при обновлении {name}: {e}")

            sleep(0.3)  # бережём API

    logger.info("🏁 Загрузка завершена")


if __name__ == "__main__":
    main()

import os
import requests
import pandas as pd
from sqlalchemy import text
from datetime import date
import time

from utils.db import get_engine
from utils.logger import get_logger

logger = get_logger("lastfm_loader", "logs/load_lastfm_top_artists.log")

# logger.info("🟢 Done")
# logger.warning("⚠️ Warning")
# logger.error("🔥 Critical")

engine = get_engine()

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
LASTFM_API_URL = "http://ws.audioscrobbler.com/2.0/"


def fetch_top_artists(country_name):
    try:
        params = {
            "method": "geo.gettopartists",
            "country": country_name,
            "api_key": LASTFM_API_KEY,
            "format": "json",
            "limit": 50
        }
        response = requests.get(LASTFM_API_URL, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.warning(f"⛔ Ошибка при запросе для {country_name}: {e}")
        return None


def insert_artist_if_new(mbid, name, conn):
    if mbid:
        exists = conn.execute(
            text("SELECT 1 FROM staging.artist WHERE mbid = :mbid"),
            {"mbid": mbid}
        ).fetchone()
        if not exists:
            conn.execute(
                text("INSERT INTO staging.artist (mbid, name) VALUES (:mbid, :name)"),
                {"mbid": mbid, "name": name}
            )
    else:
        # Проверка по имени, чтобы не вставлять 1000 анонимных Beyoncé
        exists = conn.execute(
            text("SELECT 1 FROM staging.artist WHERE mbid IS NULL AND name = :name"),
            {"name": name}
        ).fetchone()
        if not exists:
            conn.execute(
                text("INSERT INTO staging.artist (mbid, name) VALUES (NULL, :name)"),
                {"name": name}
            )



def main():
    fetch_dt = date.today()
    inserted_rows = 0
    skipped_rows = 0

    with engine.begin() as conn:
        countries = conn.execute(text("SELECT name, iso2 FROM staging.country")).fetchall()

        for country_name, iso2 in countries:
            logger.info(f"📡 Обработка страны: {country_name} ({iso2})")

            try:
                data = fetch_top_artists(country_name)
                if not data or 'topartists' not in data:
                    logger.warning(f"⚠️ Нет данных для {country_name}")
                    continue

                for index, artist_data in enumerate(data['topartists']['artist']):
                    try:
                        name = artist_data['name']
                        mbid = artist_data.get('mbid') or None
                        playcount = int(artist_data.get('playcount', 0))
                        rank = index + 1

                        # Вставка артиста
                        insert_artist_if_new(mbid, name, conn)

                        # Вставка в чарты
                        conn.execute(text("""
                            INSERT INTO staging.country_top_artists (
                                country_iso2, rank, artist_name, mbid, playcount, fetch_date
                            ) VALUES (
                                :country_iso2, :rank, :artist_name, :mbid, :playcount, :fetch_date
                            )
                            ON CONFLICT ON CONSTRAINT unique_cta_entry DO NOTHING;
                        """), {
                            "country_iso2": iso2,
                            "rank": rank,
                            "artist_name": name,
                            "mbid": mbid,
                            "playcount": playcount,
                            "fetch_date": fetch_dt
                        })
                        inserted_rows += 1

                    except Exception as e:
                        logger.warning(f"⚠️ Пропущен артист {artist_data.get('name')} ({mbid}): {e}")
                        skipped_rows += 1

                time.sleep(0.5)

            except Exception as e:
                logger.error(f"🔥 Критическая ошибка при обработке {country_name}: {e}")
                continue

    logger.info(f"🏁 Загрузка завершена. ✅ Успешно: {inserted_rows}, ⚠️ Пропущено: {skipped_rows}")


if __name__ == "__main__":
    main()

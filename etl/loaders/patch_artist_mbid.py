from sqlalchemy import text
from utils.db import get_engine
import requests


engine = get_engine()
MBID = "0383dadf-2a4e-4d10-a46a-e9e041da8eb3"  # ← вставь нужный
SCHEMA = "staging"
TABLE = "artist"

HEADERS = {"User-Agent": "MusicAtlas/1.0 (you@example.com)"}
URL = f"https://musicbrainz.org/ws/2/artist/{MBID}?fmt=json&inc=aliases+tags+ratings"


with engine.begin() as conn:
    print("🩹 Удаляем некорректный MBID у Queen...")
    conn.execute(text("""
        UPDATE staging.artist
        SET mbid = NULL
        WHERE name = 'Queen';
    """))

    conn.execute(text("""
        UPDATE staging.country_top_artists
        SET mbid = NULL
        WHERE artist_name = 'Queen';
    """))

    print("🩹 Вставляем корректный MBID у Queen...")
    conn.execute(text("""
        UPDATE staging.artist
        SET mbid = '0383dadf-2a4e-4d10-a46a-e9e041da8eb3'
        WHERE name = 'Queen';
    """))

    conn.execute(text("""
        UPDATE staging.country_top_artists
        SET mbid = '0383dadf-2a4e-4d10-a46a-e9e041da8eb3'
        WHERE artist_name = 'Queen';
    """))

print("✅ Патч для Queen применён")


response = requests.get(URL, headers=HEADERS)

if response.status_code != 200:
    print(f"⚠️ Не удалось получить данные для mbid={MBID}: {response.status_code}")
    exit()

data = response.json()

alias = data.get("aliases", [{}])[0].get("name") if data.get("aliases") else None
tags = ", ".join(tag["name"] for tag in data.get("tags", [])) if data.get("tags") else None
disambiguation = data.get("disambiguation")
type_ = data.get("type")
gender = data.get("gender")
country_code = data.get("country")

with engine.begin() as conn:
    conn.execute(text(f"""
        UPDATE {SCHEMA}.{TABLE}
        SET alias = :alias,
            disambiguation = :disambiguation,
            tags = :tags,
            type = :type,
            gender = :gender,
            country_code = :country_code
        WHERE mbid = :mbid
    """), {
        "alias": alias,
        "disambiguation": disambiguation,
        "tags": tags,
        "type": type_,
        "gender": gender,
        "country_code": country_code,
        "mbid": MBID
    })

print(f"✅ Обновлён исполнитель по mbid={MBID}")
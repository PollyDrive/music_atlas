import requests
import time
from sqlalchemy import text
from utils.db import get_engine

MB_BASE_URL = "https://musicbrainz.org/ws/2/artist/"
HEADERS = {"User-Agent": "MusicAtlas/1.0 (you@example.com)"}
engine = get_engine()
SCHEMA = "staging"
TABLE = "artist"

# Получаем артистов с mbid и хотя бы одним пустым полем для обогащения
with engine.connect() as conn:
    result = conn.execute(text(f"""
        SELECT artist_id, mbid, name, alias, disambiguation, tags, type, gender, country_code
        FROM {SCHEMA}.{TABLE}
        WHERE mbid IS NOT NULL AND length(mbid) > 0
    """))
    artists = result.fetchall()

print(f"🔍 Всего артистов с mbid: {len(artists)}")
updated_rows = []

for artist in artists:
    artist_id, mbid, name, cur_alias, cur_disamb, cur_tags, cur_type, cur_gender, cur_country = artist

    try:
        url = f"{MB_BASE_URL}{mbid}?fmt=json&inc=aliases+tags+ratings"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"⚠️ Не удалось получить данные для {name} ({mbid}) — статус {response.status_code}")
            continue

        data = response.json()

        # Только если поле в базе NULL или пусто — подставим новое
        aliases = data.get("aliases", [])
        alias = cur_alias if cur_alias else aliases[0].get("name") if aliases else None

        disambiguation = cur_disamb if cur_disamb else data.get("disambiguation")
        tags = cur_tags if cur_tags else ", ".join([t["name"] for t in data.get("tags", [])])
        type_ = cur_type if cur_type else data.get("type")
        gender = cur_gender if cur_gender else data.get("gender")
        country_code = cur_country if cur_country else data.get("country")

        with engine.begin() as conn:
            conn.execute(text(f"""
                UPDATE {SCHEMA}.{TABLE}
                SET alias = :alias,
                    disambiguation = :disambiguation,
                    tags = :tags,
                    type = :type,
                    gender = :gender,
                    country_code = :country_code
                WHERE artist_id = :artist_id
            """), {
                "alias": alias,
                "disambiguation": disambiguation,
                "tags": tags,
                "type": type_,
                "gender": gender,
                "country_code": country_code,
                "artist_id": artist_id
            })

        updated_rows.append(artist_id)
        print(f"✅ {name} ({mbid}) обогащён")
        time.sleep(.2)

        
    except Exception as e:
        print(f"❌ Ошибка при обработке {name}: {e}")

print(f"🎉 Обновлено артистов: {len(updated_rows)}")

# и сразу патч для Мэнсона
patch_query = text("""
    UPDATE staging.country_top_artist
    SET artist_name = alias
    WHERE LOWER(name) IN ('[unknown]', 'unknown', 'unknown artist')
      AND alias IS NOT NULL
      AND alias <> '';
""")


with engine.begin() as conn:
    result = conn.execute(patch_query)
print("✅ Имена [unknown] обновлены на значения из alias")
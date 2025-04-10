import os
import requests
import time
from datetime import date
from sqlalchemy import text
from utils.db import get_engine

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
LASTFM_API_URL = os.getenv("LASTFM_API_URL")

HEADERS = {"User-Agent": "MusicAtlas/1.0 (you@example.com)"}
engine = get_engine()

def get_tag_info(tag):
    params = {
        "method": "tag.getinfo",
        "tag": tag,
        "api_key": LASTFM_API_KEY,
        "format": "json"
    }
    try:
        response = requests.get(LASTFM_API_URL, params=params, headers=HEADERS)
        if response.status_code != 200:
            return None
        return response.json()
    except Exception as e:
        print(f"❌ Ошибка при запросе тега {tag}: {e}")
        return None

with engine.connect() as conn:
    # получаем уникальные теги из artist_tag
    tags_result = conn.execute(text("""
        SELECT DISTINCT tag
        FROM cleansed.artist_tag
        WHERE tag IS NOT NULL
    """))
    all_tags = set(row[0] for row in tags_result)

    # получаем уже загруженные
    loaded_result = conn.execute(text("""
        SELECT tag FROM cleansed.tag_info
    """))
    already_loaded = set(row[0] for row in loaded_result)

tags_to_load = sorted(all_tags - already_loaded)
print(f"🔍 Осталось загрузить {len(tags_to_load)} тегов")

for tag in tags_to_load:
    print(f"🌐 Обрабатываем тег: {tag}")
    data = get_tag_info(tag)
    time.sleep(.2)

    if not data or "tag" not in data:
        print(f"⚠️ Нет данных для {tag}")
        continue

    tag_data = data["tag"]
    description = tag_data.get("wiki", {}).get("summary")
    reach = tag_data.get("reach")
    taggings = tag_data.get("taggings")

    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO cleansed.tag_info (tag, description, reach, taggings, fetch_date)
            VALUES (:tag, :description, :reach, :taggings, :fetch_date)
        """), {
            "tag": tag,
            "description": description,
            "reach": reach,
            "taggings": taggings,
            "fetch_date": date.today()
        })

    print(f"✅ Загружено: {tag}")

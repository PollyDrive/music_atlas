import os
import pandas as pd
from utils.db import get_engine

# Пути к CSV-файлам
FILES = {
    "country": "./data/backups/country_backup.csv",
    "artist": "./data/backups/artist_backup.csv",
    "country_top_artists": "./data/backups/country_top_artists_backup.csv",
    "all_countries_religion": "./data/all_countries_religion.csv",
    "ihme_gbd": "./data/ihme_gbd_202504191722.csv",
    "RSF_2024_Data": "./data/RSF_2024_Data.csv",
}

SCHEMA = "staging"
engine = get_engine()

for table_name, path in FILES.items():
    if not os.path.exists(path):
        print(f"❌ Файл не найден: {path}")
        continue
    
    print(f"📥 Загружаем {table_name} из {path}...")
    df = pd.read_csv(path, keep_default_na=False)  # сохраняем 'NA' как строку

    # Превращаем все 'NA' → None только для анализа
    df = df.applymap(lambda x: None if isinstance(x, str) and x.strip() in ["", "NaN", "null"] else x)

    print(f"⬆️ Загружаем {len(df)} строк в {SCHEMA}.{table_name}...")
    df.to_sql(table_name, engine, if_exists="append", index=False, schema=SCHEMA)
    print(f"✅ {table_name} загружена")

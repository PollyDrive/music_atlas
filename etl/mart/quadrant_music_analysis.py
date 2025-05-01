import pandas as pd
from collections import Counter
from utils.db import get_engine
from sqlalchemy import text

engine = get_engine()

def analyze_quadrant_artist_tag(table1, col1, table2, col2, include_tags=True):
    # === Шаг 1: Загрузка данных ===
    df1 = pd.read_sql(f"SELECT iso2, name, {col1} FROM cleansed.{table1}", engine)
    df2 = pd.read_sql(f"SELECT iso2, {col2} FROM cleansed.{table2}", engine)
    df_top = pd.read_sql("SELECT * FROM cleansed.top_10_artist", engine)
    df_tag = pd.read_sql("SELECT * FROM cleansed.artist_tag", engine)

    # === Шаг 2: Построение квадрантов ===
    df = pd.merge(df1.dropna(), df2.dropna(), on="iso2", how="inner")
    df['A_level'] = pd.cut(df[col1], bins=[-float('inf'), df[col1].median(), float('inf')], labels=['low', 'high'])
    df['B_level'] = pd.cut(df[col2], bins=[-float('inf'), df[col2].median(), float('inf')], labels=['low', 'high'])
    df['quadrant'] = df['A_level'].astype(str) + '_' + df['B_level'].astype(str)

    # === Шаг 3: Присоединяем артистов к странам и квадрантам ===
    df_country_artist = pd.merge(df_top, df[['iso2', 'name', col1, col2, 'quadrant']], on="iso2", how="inner")

    if include_tags:
        # === Шаг 4: Присоединяем теги к артистам ===
        df_country_artist['artist_name_clean'] = df_country_artist['artist_name'].str.lower().str.strip()
        df_tag['name_clean'] = df_tag['name'].str.lower().str.strip()
        df_country_artist = df_country_artist.merge(
            df_tag[['name_clean', 'tag']],
            left_on='artist_name_clean',
            right_on='name_clean',
            how='left'
        )
    else:
        df_country_artist['tag'] = None

    # === Шаг 5: Группировка по финальному формату ===
    group_cols = ['quadrant', 'name', col1, col2, 'artist_name', 'tag']
    df_result = (
        df_country_artist
        .groupby(group_cols)
        .size()
        .reset_index(name='count')
        .rename(columns={'name': 'country', 'artist_name': 'artist'})
    )


    # Удаляем старую таблицу, если есть
    table_name = f"quadrant_{col1}__{col2}_result".lower().replace('.', '_')
    with engine.connect() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS mart.{table_name}"))
        conn.commit()
    # === Шаг 6: Сохранение ===
    
    df_result.to_sql(table_name, engine, schema="mart", if_exists="append", index=False)
    print(f"🛢️ Записано в mart.{table_name}")
    return df_result

analyze_quadrant_artist_tag('social', 'alcohol_per_capita_2019', 'social', 'depression_rate_2021')


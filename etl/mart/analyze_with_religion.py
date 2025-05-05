import pandas as pd
from sqlalchemy import text
from utils.db import get_engine

engine = get_engine()

def analyze_religion_vs_indicator(
    indicator_table: str,
    indicator_col: str,
    religion_rank: str,
    top_n: int,
    include_tags: bool
) -> pd.DataFrame:
    """
    Сравнение популярности религии и другого показателя через квадранты.

    indicator_table: имя таблицы в cleansed со вторым параметром (например, 'employment')
    indicator_col: имя числового столбца в этой таблице (например, 'unemployment')
    religion_rank: 'first' | 'second' | 'third' – какой по счёту религию брать
    top_n: сколько топ-артистов прикладывать
    include_tags: подгружать ли из cleansed.artist_tag
    """

    # --- Шаг 1: Загрузка данных по религиям ---
    pct_col = f"{religion_rank}_percent"
    rel_col = f"{religion_rank}_popular_religion"

    df_rel = pd.read_sql(text(f"""
        SELECT
          iso2,
          nation     AS country,
          {rel_col}  AS religion_name,
          {pct_col}  AS religion_percent
        FROM cleansed.nation_top_religions
        WHERE {pct_col} IS NOT NULL
    """), engine)

    # --- Шаг 2: Загрузка второго показателя ---
    df_ind = pd.read_sql(text(f"""
        SELECT
          iso2,
          name       AS country,
          {indicator_col} AS indicator_value
        FROM cleansed.{indicator_table}
        WHERE {indicator_col} IS NOT NULL
    """), engine)

    # --- Шаг 3: Объединяем и строим квадранты ---
    df = pd.merge(df_rel, df_ind, on=['iso2','country'], how='inner')
    # уровни low/high по медиане
    df['X_level'] = pd.cut(df['religion_percent'],
                           bins=[-float('inf'), df['religion_percent'].median(), float('inf')],
                           labels=['low', 'high'])
    df['Y_level'] = pd.cut(df['indicator_value'],
                           bins=[-float('inf'), df['indicator_value'].median(), float('inf')],
                           labels=['low', 'high'])
    df['quadrant'] = df['X_level'].astype(str) + '_' + df['Y_level'].astype(str)

    # --- Шаг 4: Добавляем топ-артистов ---
    df_top = pd.read_sql(text(f"""
        SELECT * FROM cleansed.top_10_artist
        WHERE rank <= {top_n}
    """), engine)
    df = df.merge(df_top, on='iso2', how='inner')

    # --- Шаг 5: Теги ---
    if include_tags:
        df_tag = pd.read_sql("SELECT * FROM cleansed.artist_tag", engine)
        df['artist_clean'] = df['artist_name'].str.lower().str.strip()
        df_tag['artist_clean'] = df_tag['name'].str.lower().str.strip()
        df = df.merge(df_tag[['artist_clean','tag']], on='artist_clean', how='left')
    else:
        df['tag'] = None

    # --- Шаг 6: Группировка и финальный вид ---
    group_cols = ['quadrant','country','religion_name','religion_percent','indicator_value','artist_name','tag']
    df_result = (
        df
        .drop_duplicates(subset=group_cols)
        .rename(columns={
            'artist_name':'artist',
            'religion_name': f'{religion_rank}_religion',
            'religion_percent': f'{religion_rank}_percent',
            'indicator_value': indicator_col
        })
        .sort_values(['quadrant','country'])
    )

    # --- Шаг 7: Сохранить в mart ---
    table_name = f"quadrant_{religion_rank}_religion__{indicator_col}".lower()
    with engine.connect() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS mart.{table_name}"))
        conn.commit()
    df_result.to_sql(table_name, engine, schema="mart", if_exists="append", index=False)
    print(f"🛢️ Результат записан в mart.{table_name}")

    return df_result



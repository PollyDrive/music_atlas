from utils.logger import get_logger
import pandas as pd
from sqlalchemy import text
from utils.db import get_engine

# Настройка логирования

engine = get_engine()
logger = get_logger("analyze_with_religion", "logs/analyze_with_religion.log")

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
    top_n: сколько топ-артистов
    include_tags: подгружать ли из cleansed.artist_tag
    """
    # --- Шаг 1: Загрузка данных по религиям ---
    pct_col = f"{religion_rank}_percent"
    rel_col = f"{religion_rank}_popular_religion"
    
    df_rel = pd.read_sql(text(f"""
        SELECT iso2,
               nation AS country,
               {rel_col} AS religion_name,
               {pct_col} AS religion_percent
        FROM cleansed.nation_top_religions
        WHERE {pct_col} IS NOT NULL
    """), engine)
    logger.info(f"Loaded df_rel rows: {len(df_rel)}")

    # --- Шаг 2: Загрузка второго показателя ---
    
    df_ind = pd.read_sql(text(f"""
        SELECT iso2,
               name AS country,
               {indicator_col} AS indicator_value
        FROM cleansed.{indicator_table}
        WHERE {indicator_col} IS NOT NULL
    """), engine)
    logger.info(f"Loaded df_ind rows: {len(df_ind)}")

    # --- Шаг 3: Объединяем по iso2 и объединяем country ---
    
    df = pd.merge(
        df_rel,
        df_ind,
        on='iso2',
        how='inner',
        suffixes=('_rel', '_ind')
    )
    logger.info(f"After merge, rows: {len(df)}")

    # Убираем дублированные country колонки, оставляем из религий
    df['country'] = df['country_rel']
    df = df.drop(columns=['country_rel', 'country_ind'])
    

    # --- Шаг 4: Строим уровни и квадранты ---
    median_rel = df['religion_percent'].median()
    median_ind = df['indicator_value'].median()
    df['X_level'] = pd.cut(
        df['religion_percent'],
        bins=[-float('inf'), median_rel, float('inf')],
        labels=['low', 'high']
    )
    df['Y_level'] = pd.cut(
        df['indicator_value'],
        bins=[-float('inf'), median_ind, float('inf')],
        labels=['low', 'high']
    )
    df['quadrant'] = df['X_level'].astype(str) + '_' + df['Y_level'].astype(str)
    

    # --- Шаг 5: Добавляем топ-артистов ---
    
    df_top = pd.read_sql(text(f"""
        SELECT * FROM cleansed.top_50_artist
        WHERE rank <= {top_n}
    """), engine)
    df = df.merge(df_top, on='iso2', how='inner')
    logger.info(f"After adding top artists, rows: {len(df)}")

    # --- Шаг 6: Теги (опционально) ---
    if include_tags:
        
        df_tag = pd.read_sql("SELECT * FROM cleansed.artist_tag", engine)
        df['artist_clean'] = df['artist_name'].str.lower().str.strip()
        df_tag['artist_clean'] = df_tag['name'].str.lower().str.strip()
        df = df.merge(df_tag[['artist_clean', 'tag']], on='artist_clean', how='left')
        logger.info(f"After merging tags, rows: {len(df)}")
    else:
        df['tag'] = None
        logger.info("Skipping tag merge (include_tags=False)")

    # --- Шаг 7: Группировка и финальный вид ---
    
    group_cols = ['quadrant', 'country', 'religion_name', 'religion_percent', 'indicator_value', 'artist_name', 'tag']
    df_result = (
        df
        .drop_duplicates(subset=group_cols)
        .rename(columns={
            'artist_name': 'artist',
            'religion_name': f'{religion_rank}_religion',
            'religion_percent': f'{religion_rank}_percent',
            'indicator_value': indicator_col
        })
        .sort_values(['quadrant', 'country'])
    )
    logger.info(f"Final result rows: {len(df_result)}")

    # --- Шаг 8: Сохранить в mart ---
    table_name = f"quadrant_{religion_rank}_religion__{indicator_col}".lower()
    
    with engine.connect() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS mart.{table_name}"))
        conn.commit()
    df_result.to_sql(table_name, engine, schema="mart", if_exists="append", index=False)
    print(f"🛢️ Записано в mart.{table_name}")

    return df_result

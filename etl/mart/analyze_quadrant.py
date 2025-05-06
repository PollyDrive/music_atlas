import pandas as pd
import gc
import numpy as np
from collections import Counter
from utils.db import get_engine
from sqlalchemy import text
from utils.memory_optimize import optimize_df_memory

engine = get_engine()

# --- --- --- --- --- #
def analyze_quadrant_artist_tag(table1, col1, table2, col2, top_n, include_tags=True):
    # === Шаг 1: Загрузка данных с использованием только нужных столбцов ===
    print(f"Loading data from {table1} and {table2}...")
    df1 = pd.read_sql_query(f"SELECT iso2, name, {col1} FROM cleansed.{table1}", engine)
    df1 = optimize_df_memory(df1)
    
    df2 = pd.read_sql_query(f"SELECT iso2, {col2} FROM cleansed.{table2}", engine)
    df2 = optimize_df_memory(df2)
    
    # Загружаем артистов с фильтрацией по rank, выбирая только нужные столбцы
    print(f"Loading top {top_n} artists...")
    df_top = pd.read_sql_query(f"""
        SELECT iso2, artist_name, rank 
        FROM cleansed.top_10_artist
        WHERE rank <= {top_n}
    """, engine)
    df_top = optimize_df_memory(df_top)
    
    # Загружаем теги только если они нужны
    if include_tags:
        print("Loading artist tags...")
        df_tag = pd.read_sql_query("SELECT name, tag FROM cleansed.artist_tag", engine)
        df_tag = optimize_df_memory(df_tag)
    # === Шаг 2: Построение квадрантов ===
    print("Building quadrants...")
    # Drop NA values before merging to reduce dataframe size
    df1_clean = df1.dropna(subset=[col1])
    df2_clean = df2.dropna(subset=[col2])
    
    # Only keep necessary columns for the merge
    df = pd.merge(df1_clean[['iso2', 'name', col1]], 
                 df2_clean[['iso2', col2]], 
                 on="iso2", how="inner")
    
    # Calculate median once to avoid recalculation
    col1_median = df[col1].median()
    col2_median = df[col2].median()
    
    df['A_level'] = pd.cut(df[col1], bins=[-float('inf'), col1_median, float('inf')], labels=['low', 'high'])
    df['B_level'] = pd.cut(df[col2], bins=[-float('inf'), col2_median, float('inf')], labels=['low', 'high'])
    df['quadrant'] = df['A_level'].astype('category') + '_' + df['B_level'].astype('category')
    
    # Clean up memory
    del df1_clean, df2_clean
    gc.collect()
    # === Шаг 3: Присоединяем артистов к странам и квадрантам ===
    print("Merging countries, artists and quadrants...")
    df_country_artist = pd.merge(
        df_top, 
        df[['iso2', 'name', col1, col2, 'quadrant']], 
        on="iso2", 
        how="inner"
    )
    
    # Free up memory
    del df, df_top
    gc.collect()
    
    if include_tags:
        print("Adding tags to artists...")
        # Convert to lowercase and strip once before merging
        df_country_artist['artist_name_clean'] = df_country_artist['artist_name'].str.lower().str.strip()
        df_tag['name_clean'] = df_tag['name'].str.lower().str.strip()
        
        # Convert to categorical to save memory before merge
        df_country_artist['artist_name_clean'] = df_country_artist['artist_name_clean'].astype('category')
        df_tag['name_clean'] = df_tag['name_clean'].astype('category')
        
        # Only keep necessary columns for the merge
        df_country_artist = df_country_artist.merge(
            df_tag[['name_clean', 'tag']],
            left_on='artist_name_clean',
            right_on='name_clean',
            how='left'
        )
        
        # Free up memory
        del df_tag
        gc.collect()
    else:
        df_country_artist['tag'] = None

    # === Шаг 5: Группировка по финальному формату ===
    print("Grouping data...")
    # Convert string columns to category before groupby to save memory
    for col in ['quadrant', 'name', 'artist_name', 'tag']:
        if col in df_country_artist.columns and df_country_artist[col].dtype == 'object':
            df_country_artist[col] = df_country_artist[col].astype('category')
    
    group_cols = ['quadrant', 'name', col1, col2, 'artist_name', 'tag']
    df_result = (
        df_country_artist
        .groupby(group_cols, observed=True)  # Add observed=True parameter
        .size()
        .reset_index(name='count')
        .drop(columns=["count"]) 
        .rename(columns={'name': 'country', 'artist_name': 'artist'})
    )
    
    # Free up memory
    del df_country_artist
    gc.collect()


    # Удаляем старую таблицу, если есть
    table_name = f"quadrant_{col1}__{col2}_result".lower().replace('.', '_')
    with engine.connect() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS mart.{table_name}"))
        conn.commit()
    # === Шаг 6: Сохранение ===
    
    df_result.to_sql(table_name, engine, schema="mart", if_exists="append", index=False)
    print(f"🛢️ Записано в mart.{table_name}")
    return df_result


# --- --- --- --- --- #

def analyze_single_indicator(table, column, top_n=10, include_tags=True):
    print(f"Analyzing {column} from {table}...")
    
    # === Шаг 1: Загрузка и очистка таблицы
    print(f"Loading data from {table}...")
    df = pd.read_sql_query(f"SELECT iso2, name, {column} FROM cleansed.{table}", engine)
    df = optimize_df_memory(df)
    df = df.dropna(subset=[column])
    
    if include_tags:
        print("Loading artist tags...")
        df_tag = pd.read_sql_query("SELECT name, tag FROM cleansed.artist_tag", engine)
        df_tag = optimize_df_memory(df_tag)
    
    # === Шаг 2: Деление
    print("Computing median splits...")
    df['median'] = pd.qcut(df[column], 2, labels=["Q1", "Q2"]).astype('category')
    
    # === Шаг 3: Загрузка артистов и фильтрация по top_n
    print(f"Loading top {top_n} artists...")
    df_artists = pd.read_sql_query(f"""
        SELECT iso2, artist_name, rank
        FROM cleansed.top_50_artist
        WHERE rank <= {top_n}
    """, engine)
    df_artists = optimize_df_memory(df_artists)
    print("Merging countries and artists...")
    df_country_artist = pd.merge(df_artists, df[['iso2', 'name', column, 'median']], on="iso2", how="inner")
    
    # Free up memory
    del df, df_artists
    gc.collect()  # Added parentheses to actually call the function

    # === Шаг 4: Add tags if requested
    if include_tags:
        print("Adding tags to artists...")
        # Convert to lowercase and strip once before merging
        df_country_artist['artist_name_clean'] = df_country_artist['artist_name'].str.lower().str.strip()
        df_tag['name_clean'] = df_tag['name'].str.lower().str.strip()
        
        # Convert to categorical to save memory before merge
        df_country_artist['artist_name_clean'] = df_country_artist['artist_name_clean'].astype('category')
        df_tag['name_clean'] = df_tag['name_clean'].astype('category')
        
        # Only keep necessary columns for the merge
        df_country_artist = df_country_artist.merge(
            df_tag[['name_clean', 'tag']],
            left_on='artist_name_clean',
            right_on='name_clean',
            how='left'
        )
        
        # Free up memory
        del df_tag
        gc.collect()
    else:
        df_country_artist['tag'] = None

    # === Шаг 5: Финальная агрегация
    # Convert string columns to category before groupby to save memory
    for col in ['median', 'name', 'artist_name']:
        if col in df_country_artist.columns and df_country_artist[col].dtype == 'object':
            df_country_artist[col] = df_country_artist[col].astype('category')
    
    if 'tag' in df_country_artist.columns and df_country_artist['tag'].dtype == 'object':
        df_country_artist['tag'] = df_country_artist['tag'].astype('category')

    # Only include tag in group_cols if include_tags is True
    group_cols = ['median', 'name', column, 'artist_name', 'rank']
    if include_tags:
        group_cols.append('tag')

    df_result = (
        df_country_artist
        .groupby(group_cols, observed=True)  # Add observed=True parameter
        .size()
        .reset_index(name='count')
        .drop(columns=["count"]) 
        .rename(columns={'name': 'country', 'artist_name': 'artist'})
    )
    
    # Free up memory
    del df_country_artist
    gc.collect()

    # Удаляем старую таблицу, если есть
    table_name = f"median_{column}_result".lower().replace('.', '_')
    with engine.connect() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS mart.{table_name}"))
        conn.commit()
    # === Шаг 6: Сохранение ===
    
    df_result.to_sql(table_name, engine, schema="mart", if_exists="append", index=False)
    print(f"🛢️ Записано в mart.{table_name}")
    return df_result
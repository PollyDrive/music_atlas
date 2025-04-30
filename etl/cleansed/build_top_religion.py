import logging
from sqlalchemy import text
from utils.db import get_engine


# Но проверять ее я уже не буду, тяни с бэкапа

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def generate_top_religions_query(nation_column: str, religion_cols: list, source_table: str, target_table: str) -> str:
    try:
        if not religion_cols or not nation_column:
            raise ValueError("Список религий или название колонки нации не указаны.")

        if not source_table or not target_table:
            raise ValueError("Имена исходной и целевой таблиц должны быть заданы.")

        sql_parts = []
        for religion_col in religion_cols:
            percent_col = f"{religion_col}_percent"
            part = (
                f"SELECT {nation_column}, iso2, '{religion_col}' AS religion_name, "
                f"REGEXP_REPLACE({religion_col}::TEXT, '\\D', '', 'g')::NUMERIC AS religion_population, {percent_col} AS religion_percent "
                f"FROM {source_table} "
                f"WHERE {religion_col} IS NOT NULL AND {percent_col} IS NOT NULL"
            )
            sql_parts.append(part)

        unpivot_query = "\nUNION ALL\n".join(sql_parts)

        full_query = f"""
        DROP TABLE IF EXISTS {target_table};
CREATE TABLE IF NOT EXISTS {target_table} (
    nation VARCHAR(255),
    iso2 CHAR(2),
    first_popular_religion VARCHAR(255),
    first_population numeric,
    first_percent DECIMAL(5,2),
    second_popular_religion VARCHAR(255),
    second_population numeric,
    second_percent DECIMAL(5,2),
    third_popular_religion VARCHAR(255),
    third_population numeric,
    third_percent DECIMAL(5,2)
);

WITH unpivoted AS (
    {unpivot_query}
),
ranked AS (
    SELECT
        nation,
        iso2,
        religion_name,
        religion_population,
        religion_percent,
        ROW_NUMBER() OVER (PARTITION BY {nation_column} ORDER BY religion_percent DESC) AS rn
    FROM unpivoted
)

INSERT INTO {target_table} (nation, iso2, first_popular_religion, first_population, first_percent, second_popular_religion, second_population, second_percent, third_popular_religion, third_population, third_percent)
SELECT
    r1.nation,
    r1.iso2,
    r1.religion_name AS first_popular_religion,
    r1.religion_population AS first_population,
    r1.religion_percent AS first_percent,
    r2.religion_name AS second_popular_religion,
    r2.religion_population AS second_population,
    r2.religion_percent AS second_percent,
    r3.religion_name AS third_popular_religion,
    r3.religion_population AS third_population,
    r3.religion_percent AS third_percent
FROM
    ranked r1
LEFT JOIN ranked r2 ON r1.nation = r2.nation AND r2.rn = 2
LEFT JOIN ranked r3 ON r1.nation = r3.nation AND r3.rn = 3
WHERE r1.rn = 1;
"""
        logging.info("SQL-запрос успешно сгенерирован.")
        return full_query.strip()

    except Exception as e:
        logging.error(f"Ошибка при генерации SQL запроса: {e}")
        return ""

def execute_query_sqlalchemy(engine, query: str):
    try:
        with engine.connect() as connection:
            for statement in query.split(";"):
                if statement.strip():
                    connection.execute(text(statement))
            connection.commit()
        logging.info("SQL-запрос успешно выполнен в базе данных.")

    except Exception as e:
        logging.error(f"Ошибка при выполнении SQL запроса: {e}")

if __name__ == "__main__":
    # Список религий
    religion_columns = ['bahai', 'buddhists', 'chinese_folk', 'christians', 'confucianist', 'daoist', 'ethnic_religionist', 'hindus', 'jews', 'muslims', 'non_religious', 'sikhs']
    nation_col = "nation"
    source_table_name = "staging.all_countries_religion"
    target_table_name = "cleansed.nation_top_religions"

    engine = get_engine()
    
    query = generate_top_religions_query(nation_col, religion_columns, source_table_name, target_table_name)

    if query:
        execute_query_sqlalchemy(engine, query)

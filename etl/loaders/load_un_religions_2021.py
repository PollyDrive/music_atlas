# """
# load_un_religions_2021.py
# Парсит таблицу религий с UNdata и сохраняет в PostgreSQL (или CSV)
# """

# import pandas as pd
# import re
# from sqlalchemy import text
# from utils.db import get_engine

# URL = "https://data.un.org/Data.aspx?d=POP&f=tableCode%3A28%3BrefYear%3A2021"

# # ── 1. Чтение HTML-таблицы со страницы ──────────────────────────────────────
# tables = pd.read_html(URL, header=0)
# df = tables[0]   # таблица сразу на странице

# # ── 2. Очистка и переименование колонок ─────────────────────────────────────
# df = df.rename(columns={
#     "Country or Area": "country",
#     "Subgroup": "religion",
#     "Value": "percent",
#     "Unit": "unit"
# })

# # ── 3. Убираем строчки без значения
# df = df[df["percent"].notna() & (df["unit"] == "PERCENT")]
# df["percent"] = df["percent"].astype(float)

# # ── 4. Приводим названия религий к нижнему регистру + заменяем пробелы на _
# df["religion"] = (
#     df["religion"]
#     .str.lower()
#     .str.replace(r"[^\w\s]", "", regex=True)
#     .str.replace(r"\s+", "_", regex=True)
# )

# # ── 5. (опц.) pivot: строки — страны, колонки — религии ─────────────────────
# pivot = df.pivot_table(index="country", columns="religion", values="percent", aggfunc="sum").reset_index()
# pivot.columns.name = None  # убрать 'religion' сверху

# # ── 6. (опц.) сохранить в базу ──────────────────────────────────────────────
# engine = get_engine()
# with engine.begin() as conn:
#     conn.execute(text("DROP TABLE IF EXISTS staging.un_religions CASCADE"))
#     pivot.to_sql("un_religions", conn, schema="staging", index=False)

# print(f"✓ Загрузили {len(df)} строк религиозных данных из UN → staging.un_religions")

# # ── 7. (альт.) сохранить как CSV ────────────────────────────────────────────
# pivot.to_csv("/mnt/data/un_religions_by_country_2021.csv", index=False)


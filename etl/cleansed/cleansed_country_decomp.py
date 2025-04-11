import pandas as pd
from sqlalchemy import text
from utils.db import get_engine

engine = get_engine()

with open("sql/schemas/create_cleansed_country.sql", "r") as f:
    sql = f.read()

with engine.begin() as conn:
    conn.execute(text(sql))

print("✅ Таблицы country в cleansed созданы!")
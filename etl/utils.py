import os
import logging
from dotenv import load_dotenv

# Загрузка .env
load_dotenv()

# Подключение к БД
# engine = create_engine(get_db_url())

# # Достаем список стран из таблицы country_dict
# query = "SELECT name FROM staging.country_dict"
# countries_df = pd.read_sql(query, con=engine)
# country_names = countries_df['name'].tolist()


# Настройка логгинга
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def get_db_url():
    return f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"



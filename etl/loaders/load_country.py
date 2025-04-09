from utils import logging   # <--- вот где вызывается utils
import pandas as pd
import requests
import os
import time
from utils.db import get_engine
from utils.logger import get_logger

logger = get_logger("country_loader", "logs/load_country.log")
engine = get_engine()

API_KEY = os.getenv('API_NINJAS_KEY')
headers = {'X-Api-Key': API_KEY}

def main():
    logging.info("=== START country loader ===")
    
    # Загружаем список стран с ISO2
    iso_df = pd.read_sql("SELECT country_common, iso2 FROM staging.iso_countries", con=engine)
    # Уже загруженные iso2
    existing_iso2 = pd.read_sql("SELECT iso2 FROM staging.country", con=engine)['iso2'].tolist()
    # Словарь country -> iso2
    country_to_iso2 = dict(zip(iso_df['country_common'], iso_df['iso2']))

    country_names = iso_df['country_common'].tolist()
    logging.info(f"Number of countries: {len(country_names)}")
    # country_names = ['United States of America', 'Sweden'] # для отладки чтобы не дергать апи
    all_data = []

    for country in country_names:
        logging.info(f"Requesting: {country}")
        country_iso2 = country_to_iso2.get(country)
        if country_iso2 in existing_iso2:
            logging.info(f"⏩ {country} (ISO2={country_iso2}) уже есть в staging.country, пропускаем")
            continue

        response = requests.get(
            "https://api.api-ninjas.com/v1/country",
            headers=headers,
            params={"name": country}
        )
        if response.status_code == 200:
            data = response.json()
            if data:
                item = data[0]
                # --- подготовка данных без вложенных ---
                item_flat = {
                    **{k: v for k, v in item.items() if not isinstance(v, dict)},  # без вложенных
                    "currency_code": item.get("currency", {}).get("code"),
                    "currency_name": item.get("currency", {}).get("name")
                }
                
                df = pd.DataFrame([item_flat])
                df.to_sql('country', schema='staging', con=engine, if_exists='append', index=False)
                logging.info(f"✅ Загружено в БД: {country}")
            else:
                logging.warning(f"Пустой ответ для {country}")
        else:
            logging.warning(f"❌ Ошибка для {country}: {response.status_code} - {response.text}")

        time.sleep(0.3)

    if all_data:
        df = pd.json_normalize(all_data)
        df.to_sql('country', schema='staging', con=engine, if_exists='append', index=False)
        logging.info("=== Data loaded successfully ===")
    else:
        logging.warning("No data received")

    logging.info("=== END country loader ===")
if __name__ == "__main__":
    main()

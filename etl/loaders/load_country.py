from etl.utils import get_db_url, logging   # <--- вот где вызывается utils
import pandas as pd
import requests
import os
import time
from sqlalchemy import create_engine

API_KEY = os.getenv('API_NINJAS_KEY')
headers = {'X-Api-Key': API_KEY}

def main():
    logging.info("=== START country loader ===")
    engine = create_engine(get_db_url())
    
    countries_df = pd.read_sql("SELECT country_common FROM staging.iso_countries", con=engine)
    # country_names = countries_df['country_common'].tolist()
    # logging.info(f"Number of countries: {len(country_names)}")
    country_names = ['United States of America', 'Sweden']
    all_data = []

    for country in country_names:
        logging.info(f"Requesting: {country}")
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
                all_data.append(item_flat)
                logging.info(f"✅ Данные для {country} получены")
            else:
                logging.warning(f"Пустой ответ для {country}")
        else:
            logging.warning(f"❌ Ошибка для {country}: {response.status_code} - {response.text}")

        time.sleep(0.5)

    if all_data:
        df = pd.json_normalize(all_data)
        df.to_sql('country', schema='staging', con=engine, if_exists='append', index=False)
        logging.info("=== Data loaded successfully ===")
    else:
        logging.warning("No data received")

    logging.info("=== END country loader ===")

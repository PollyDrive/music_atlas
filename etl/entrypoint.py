import logging
from etl.loaders import load_country
# from etl import load_genre, load_author  # добавишь позже

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def main():
    logging.info("=== ETL PIPELINE START ===")
    
    # Step 1: Country Loader
    try:
        load_country.main()
        logging.info("Country load finished successfully.")
    except Exception as e:
        logging.error(f"Country loader failed: {e}")

    # Step 2: Genre Loader (заготовка)
    # try:
    #     load_genre.main()
    #     logging.info("Genre load finished successfully.")
    # except Exception as e:
    #     logging.error(f"Genre loader failed: {e}")

    # Step 3: Author Loader (заготовка)
    # try:
    #     load_author.main()
    #     logging.info("Author load finished successfully.")
    # except Exception as e:
    #     logging.error(f"Author loader failed: {e}")

    logging.info("=== ETL PIPELINE FINISHED ===")

if __name__ == "__main__":
    main()

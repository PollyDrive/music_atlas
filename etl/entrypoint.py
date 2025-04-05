import logging
from etl.loaders import load_country
from etl.loaders import load_lastfm_top_artists
# from etl import load_genre, load_author  # добавишь позже

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s",
# )

def main():
    logging.info("=== ETL PIPELINE START ===")
    
    # Step 1: Country Loader
    try:
        load_country.main()
        logging.info("Country load finished successfully.")
    except Exception as e:
        logging.error(f"Country loader failed: {e}")

    # Step 2: Genre Loader (заготовка)
    try:
        load_lastfm_top_artists.main()
        logging.info("Genre load finished successfully.")
    except Exception as e:
        logging.error(f"Genre loader failed: {e}")

    # Step 3: Artist Loader (заготовка)
    try:
        load_artist_info.main()
        logging.info("Artist load finished successfully.")
    except Exception as e:
        logging.error(f"Artist loader failed: {e}")

    logging.info("=== ETL PIPELINE FINISHED ===")

if __name__ == "__main__":
    main()

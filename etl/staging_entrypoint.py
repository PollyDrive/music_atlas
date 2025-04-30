import logging
from etl.loaders import load_country
from etl.loaders import load_lastfm_top_artists
from etl.loaders import load_artist_info
from etl.loaders import load_artist_tags_from_lastfm
from etl.cleansed import load_tag_info_lastfm
from etl.loaders import load_artist_musicbrainz
from etl.loaders import patch_artist_mbid
from etl.enrich import load_alcohol_consumption
from etl.enrich import load_country_languages
from etl.enrich import load_depression_rate
from etl.enrich import load_press_freedom
from etl.enrich import load_suicide_rate
from etl import pre_cleanup_artists


def main():
    logging.info("=== STAGING PIPELINE START ===")
    
    # Грузим инфу о всех странам из ninja api (по iso_countries)
    try:
        load_country.main()
        logging.info("Country load finished successfully.")
    except Exception as e:
        logging.error(f"Country loader failed: {e}")

    # ----------------м-у-з-л-о-------------------- #

    # По всем странам берем топ-50 из Last.fm
    try:
        load_lastfm_top_artists.main()
        logging.info("Charts load finished successfully.")
    except Exception as e:
        logging.error(f"Charts loader failed: {e}")

    # По всем исполнителям из чартов заполняем инфу о них с Last.fm
    try:
        load_artist_info.main()
        logging.info("Artist load finished successfully.")
    except Exception as e:
        logging.error(f"Artist loader failed: {e}")

    # Обогащение исполнителя жанрами
    try:
        load_artist_tags_from_lastfm.main()
        logging.info("Artist genres load finished successfully.")
    except Exception as e:
        logging.error(f"Artist genres loader failed: {e}")
    
    # Обогащение исполнителей из musicbrainz (artist_musicbrainz)
    try:
        load_artist_musicbrainz.main()
        logging.info("Artist enrich finished successfully.")
    except Exception as e:
        logging.error(f"Artist enrich failed: {e}")
    
    # Если надо, то патч на кривые данные (но не все)
    try:
        patch_artist_mbid.main()
        logging.info("Artist patch finished successfully.")
    except Exception as e:
        logging.error(f"Artist patch failed: {e}")

    # ----------------м-у-з-л-о-------------------- #

    # Обогащение статистикой алкоголя на душу, депрессивных заболеваний,
    # свободы прессы, уровня суицида и основных языков, все в country
    try:
        load_alcohol_consumption.main()
        load_country_languages.main()
        load_depression_rate.main()
        load_press_freedom.main()
        load_suicide_rate.main()
        logging.info("Country enrich finished successfully.")
    except Exception as e:
        logging.error(f"Country enrich failed: {e}")

    # И еще один патч для исполнителей с невалидными именами и валидным alias
    try:
        pre_cleanup_artists.main()
    except Exception as e:
        logging.error(f"Artist patch failed: {e}")

    logging.info("=== STAGING PIPELINE FINISHED ===")

    # После сохранения накатывать обратно в пстгр
    # python3 -m etl.loaders.csv_to_postgres

if __name__ == "__main__":
    main()

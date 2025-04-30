import logging
from etl.cleansed import build_artist_tag_lastfm
from etl.cleansed import load_tag_info_lastfm
from etl.cleansed import build_top_religion

def main():
    logging.info("=== CLEANSED PIPELINE START ===")

    # ----------------м-у-з-л-о-------------------- #
    # Нормализация тегов в artists. Сопоставляю пары исполнитель-жанр.
    try:
        build_artist_tag_lastfm.main()
        logging.info("Genres load finished successfully.")
    except Exception as e:
        logging.error(f"Genres loader failed: {e}")

    # Добавляем описание найденным жанрам в новую таблицу. Беспонтовая, пока не пригодилась.
    try:
        load_tag_info_lastfm.main()
        logging.info("Genres load finished successfully.")
    except Exception as e:
        logging.error(f"Genres loader failed: {e}")

    # Топ-3 религий (кол-во и проц.соотношение) для всех стран
    try:
        build_top_religion.main()
        logging.info("Genres load finished successfully.")
    except Exception as e:
        logging.error(f"Genres loader failed: {e}")

        
    
    logging.info("=== CLEANSED PIPELINE FINISHED ===")

if __name__ == "__main__":
    main()

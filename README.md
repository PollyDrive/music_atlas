Music Atlas is a platform for wacky correlations that shows various weird connections between the popularity of artists or genres and various country metrics.
For example:
- Comparing the number of k-pop concerts and the suicide rate.
- What exactly does a "sex playlist" mean in different countries?
- Comparing the birth rate and the popularity of new metal bands in the early 2000s.
- The influence of the economic system on the popularity of the chanson genre.
- The relationship between the divorce rate and the popularity of breakup songs

In the future, we plan to:
- Collect song data (metadata + lyrics) from various open music databases.
- Research connections (song ↔ author ↔ genre ↔ country ↔ year).
- Correlations and statistics on graphs by year.


Music Atlas — это платформа для дурацких корреляций, которая показывает различные странные связи между популярностью исполнителей или жанров и различными показателями страны.
Например:
- Сравнение количества концертов k-pop и уровня самоубийств.
- Что именно означает «секс-плейлист» в разных странах?
- Сравнение уровня рождаемости и популярности новых метал-групп в начале нулевых.
- Влияние экономической системы на популярность жанра «шансон».
- Связь между количеством разводов и популярностью песен о расставаниях

В будущем планируется:
- сбор данных о песнях (метаданные + тексты) из различных открытых баз данных музыки.
- исследование связей (песня ↔ автор ↔ жанр ↔ страна ↔ год).
- корреляции и статистика на графиках по годам.

## Стек
PostgreSQL, 
Docker, 
Python ≥ 3.10, 
pandas, 
SQLAlchemy, 
psycopg2, 
Alembic 

## Инициализация
1. получи все необходимые ключи (API_NINJAS_KEY, LASTFM_API_KEY)
2. Таблица iso_country заполняется сразу при создании схем
3. После успешного заполнения базы сохрани все csv в /data
   Ожидаемые пути:
    `./data/country.csv`
    `./data/artist.csv`
    `./data/country_top_artists_backup.csv`


`docker-compose up --build`

`'python3 -m etl.staging_entrypoint`
запустит 3 лоадера на внешние адреса


## Повторный запуск
`docker-compose up --build`

`python3 -m etl.loaders.csv_country_top_to_postgres`
1. читает country.csv, artist.csv, country_top_artists_backup.csv
2. обрабатывает значения 'NA' (!) и null
3. загружает данные в таблицы staging.country, staging.artist, staging.country_top_artists

`alembic upgrade head` 
Накатит обновления по табличкам

`python3 -m etl.loaders.load_artist_tags_from_lastfm` 
На случай, если в первый раз ласт проебал теги

`python3 -m etl.loaders.patch_artist_mbid` 
Костыль для группы Queen, для которой last.fm отдаёт неправильный mbid японской девочки Tomomi Itano 

### Next step

`python3 -m etl.cleansed.build_artist_tag_lastfm`
Сопоставляю исполнителя с жанрами, делю строку тегов на отдельные жанры

`python3 -m etl.cleansed.load_tag_info_lastfm.py`
Загружаю подробную инфу про жанры

### Витрины
`python3 -m etl.mart_entrypoint.py` разбивает country по тематикам
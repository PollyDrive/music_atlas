!DEPRECATED!
Инициализация c 0

1. получи ключи API_NINJAS_KEY, LASTFM_API_KEY, внеси в энв

## Старт c 0
1. `docker-compose up --build` запустит инстанс PostgreSql и Metabase

2. Таблица iso_country создается и заполняется при инициализации.

3. `'python3 -m etl.staging_entrypoint`
   Пояснение в `docs/staging_description.md`

4. После успешного заполнения всех таблиц сохрани все в csv в /data
   Ожидаемые таблицы:
    `./data/iso_countries.csv`
    `./data/backups/country.csv`
    `./data/backups/artist.csv`
    `./data/backups/country_top_artists_backup.csv`
    `./data/all_countries_religion.csv`
    `./data/ihme_gbd.csv`



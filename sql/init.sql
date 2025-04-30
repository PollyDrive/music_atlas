-- -- init.sql старт и для staging и для cleansed

\echo '==> Resetting database...'
\i '/docker-entrypoint-initdb.d/utils/dev_reset.sql'

\echo '==> Creating staging schema and tables...'
\i '/docker-entrypoint-initdb.d/migrations/staging/v001__create_staging.sql'

\echo '==> Creating indices...'
\i '/docker-entrypoint-initdb.d/utils/v001__indices.sql' --по идее, они не нужны, но ради примера пусть останутся

-----------------

-- \echo '==> Loading data...'
-- \echo '==> Creating iso-countries'
\i '/docker-entrypoint-initdb.d/schemas/iso_countries.sql'
\i '/docker-entrypoint-initdb.d/migrations/staging/V002__add_fields.sql'
\i '/docker-entrypoint-initdb.d/migrations/staging/v003__create_indices.sql'
\i '/docker-entrypoint-initdb.d/migrations/staging/v004__create_enrich.sql'

---- cleansed ---- 

\echo '==> Creating cleansed schema and tables...'
\i '/docker-entrypoint-initdb.d/migrations/cleansed/v001__create_cleansed_schemas.sql'
\i '/docker-entrypoint-initdb.d/migrations/cleansed/v001__create_cleansed_country.sql'


--план такой:
-- 1. Запустить скрипт создания всех необходимых для стейджинга схем
-- 2. Очистить таблицы от говна
-- 3. Проверить созданные схемы
-- 4. Дописать недостающие
-- 5. Проверить индексы, ключи
-- 6. Накатить бэкап
--~~Сделать: country_language~~


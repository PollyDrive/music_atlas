-- dev-reset.sql
-- Быстро сбрасываем и пересоздаем всё для локальной разработки

-- Drop схем
DROP SCHEMA IF EXISTS staging CASCADE;
DROP SCHEMA IF EXISTS cleansed CASCADE;
DROP SCHEMA IF EXISTS analytics CASCADE;


DROP TABLE IF EXISTS staging.song CASCADE;
DROP TABLE IF EXISTS staging.album CASCADE;
DROP TABLE IF EXISTS staging.artist CASCADE;
DROP TABLE IF EXISTS staging.genre CASCADE;
DROP TABLE IF EXISTS staging.country CASCADE;

-- -- Создаем схемы заново
-- CREATE SCHEMA staging;
-- CREATE SCHEMA cleansed;
-- CREATE SCHEMA analytics;

-- -- Подключаем схемы как в init
-- \i schemas/create_staging.sql
-- \i schemas/indices.sql
-- \i seeds/seed_test_data.sql

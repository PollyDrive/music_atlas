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
DROP TABLE IF EXISTS staging.iso_countries CASCADE;
DROP TABLE IF EXISTS staging.country CASCADE;



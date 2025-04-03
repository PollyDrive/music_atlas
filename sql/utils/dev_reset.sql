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
-- DROP TABLE IF EXISTS staging.iso_countries CASCADE;
-- DROP TABLE IF EXISTS staging.country CASCADE;


-- Очистить таблицы
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'staging') THEN
        -- Только если схема есть
        IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'staging' AND tablename = 'country') THEN
            TRUNCATE TABLE staging.country CASCADE;
        END IF;

        IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'staging' AND tablename = 'iso_countries') THEN
            TRUNCATE TABLE staging.iso_countries CASCADE;
        END IF;
    ELSE
        RAISE NOTICE 'Схема staging не найдена. Пропускаю очистку.';
    END IF;
END$$;

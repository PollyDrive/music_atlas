-- dev-reset.sql

DROP SCHEMA IF EXISTS staging CASCADE;
DROP SCHEMA IF EXISTS cleansed CASCADE;
DROP SCHEMA IF EXISTS mart CASCADE;

DROP TABLE IF EXISTS staging.iso_countries CASCADE;
DROP TABLE IF EXISTS staging.country CASCADE;
DROP TABLE IF EXISTS staging.artist CASCADE;
DROP TABLE IF EXISTS staging.country_top_artists CASCADE;
DROP TABLE IF EXISTS staging.country_religion CASCADE;
DROP TABLE IF EXISTS staging.ihme_gbd CASCADE;


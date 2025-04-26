DROP SCHEMA IF NOT EXISTS cleansed;
CREATE SCHEMA IF NOT EXISTS cleansed;

DROP TABLE IF EXISTS cleansed.life_value;
DROP TABLE IF EXISTS cleansed.population;
DROP TABLE IF EXISTS cleansed.gdp;
DROP TABLE IF EXISTS cleansed.education;
DROP TABLE IF EXISTS cleansed.employment;
DROP TABLE IF EXISTS cleansed.others;


---сначала дропаем дубликаты
DELETE FROM staging.country a
USING (
  SELECT MIN(ctid) as keep_ctid, name, iso2, region
  FROM staging.country
  GROUP BY name, iso2, region
  HAVING COUNT(*) > 1
) dup
WHERE a.name = dup.name
  AND a.iso2 = dup.iso2
  AND a.region = dup.region
  AND a.ctid <> dup.keep_ctid;



CREATE TABLE cleansed.life_value AS
SELECT
    iso2,
    name,
    region,
    life_expectancy_female,
    life_expectancy_male,
    fertility,
    infant_mortality
FROM staging.country;

CREATE TABLE cleansed.population AS
SELECT
    iso2,
    name,
    region,
    population,
    surface_area,
    pop_density,
    pop_growth,
    urban_population,
    urban_population_growth,
    sex_ratio,
    refugees,
    tourists
FROM staging.country;

CREATE TABLE cleansed.gdp AS
SELECT
    iso2,
    name,
    region,
    gdp,
    gdp_per_capita,
    gdp_growth,
    exports,
    imports
FROM staging.country;

CREATE TABLE cleansed.education AS
SELECT
    iso2,
    name,
    region,
    primary_school_enrollment_male,
    primary_school_enrollment_female,
    secondary_school_enrollment_male,
    secondary_school_enrollment_female,
    post_secondary_enrollment_male,
    post_secondary_enrollment_female
FROM staging.country;


CREATE TABLE cleansed.employment AS
SELECT
    iso2,
    name,
    region,
    employment_agriculture,
    employment_industry,
    employment_services,
    unemployment
FROM staging.country;


CREATE TABLE cleansed.others AS
SELECT
    iso2,
    name,
    region,
    internet_users,
    homicide_rate,
    co2_emissions,
    threatened_species,
    forested_area,
    currency_code,
    currency_name
FROM staging.country;

CREATE TABLE cleansed.social AS
SELECT
    iso2,
    name,
    region,
    majority_religion,
    languages,
    press_freedom_2024,
    suicide_rate_2021,
    depression_rate_2021,
    alcohol_per_capita_2019
FROM staging.country;

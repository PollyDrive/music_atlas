DROP SCHEMA IF NOT EXISTS cleansed;
CREATE SCHEMA IF NOT EXISTS cleansed;

DROP TABLE IF EXISTS cleansed.country;
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

CREATE TABLE IF NOT EXISTS cleansed.country (
	iso2 char(2) PRIMARY KEY,
	name VARCHAR(50) NOT NULL,
    region VARCHAR(50)
)
insert into cleansed.country
SELECT
    iso2,
    name,
    region
FROM staging.country


CREATE TABLE cleansed.life_value AS
SELECT
    iso2,
    life_expectancy_female,
    life_expectancy_male,
    fertility,
    infant_mortality,
    FOREIGN KEY (iso2) REFERENCES cleansed.country(iso2);
FROM staging.country;

CREATE TABLE cleansed.population AS
SELECT
    iso2,
    population,
    surface_area,
    pop_density,
    pop_growth,
    urban_population,
    urban_population_growth,
    sex_ratio,
    refugees,
    tourists.
    FOREIGN KEY (iso2) REFERENCES cleansed.country(iso2);
FROM staging.country;

CREATE TABLE cleansed.gdp AS
SELECT
    iso2,
    gdp,
    gdp_per_capita,
    gdp_growth,
    exports,
    imports,
    FOREIGN KEY (iso2) REFERENCES cleansed.country(iso2);
FROM staging.country;

CREATE TABLE cleansed.education AS
SELECT
    iso2,
    primary_school_enrollment_male,
    primary_school_enrollment_female,
    secondary_school_enrollment_male,
    secondary_school_enrollment_female,
    post_secondary_enrollment_male,
    post_secondary_enrollment_female,
    FOREIGN KEY (iso2) REFERENCES cleansed.country(iso2);
FROM staging.country;

CREATE TABLE cleansed.employment AS
SELECT
    iso2,
    employment_agriculture,
    employment_industry,
    employment_services,
    unemployment,
    FOREIGN KEY (iso2) REFERENCES cleansed.country(iso2);
FROM staging.country;


CREATE TABLE cleansed.others AS
SELECT
    iso2,
    internet_users,
    homicide_rate,
    co2_emissions,
    threatened_species,
    forested_area,
    currency_code,
    currency_name,
    FOREIGN KEY (iso2) REFERENCES cleansed.country(iso2);
FROM staging.country;

CREATE TABLE cleansed.social AS
SELECT
    iso2,
    languages,
    press_freedom_2024,
    suicide_rate_2021,
    depression_rate_2021,
    depression_value_2021,
    alcohol_per_capita_2019,
    FOREIGN KEY (iso2) REFERENCES cleansed.country(iso2);
FROM staging.country;

ALTER TABLE cleansed.life_value
ADD CONSTRAINT fk_life_value_country
FOREIGN KEY (iso2) REFERENCES cleansed.country(iso2);

ALTER TABLE cleansed.gdp
ADD CONSTRAINT fk_gdp_country
FOREIGN KEY (iso2) REFERENCES cleansed.country(iso2);

ALTER TABLE cleansed.education
ADD CONSTRAINT fk_education_country
FOREIGN KEY (iso2) REFERENCES cleansed.country(iso2);

ALTER TABLE cleansed.population
ADD CONSTRAINT fk_population_country
FOREIGN KEY (iso2) REFERENCES cleansed.country(iso2);

ALTER TABLE cleansed.employment
ADD CONSTRAINT fk_employment_country
FOREIGN KEY (iso2) REFERENCES cleansed.country(iso2);

ALTER TABLE cleansed.others
ADD CONSTRAINT fk_othersp_country
FOREIGN KEY (iso2) REFERENCES cleansed.country(iso2);

ALTER TABLE cleansed.social
ADD CONSTRAINT fk_social_country
FOREIGN KEY (iso2) REFERENCES cleansed.country(iso2);


CREATE INDEX idx_depression_iso2 ON cleansed.life_value (iso2);
CREATE INDEX idx_population_iso2 ON cleansed.population (iso2);
CREATE INDEX idx_gdp_iso2 ON cleansed.gdp (iso2);
CREATE INDEX idx_education_iso2 ON cleansed.education (iso2);
CREATE INDEX idx_employment_iso2 ON cleansed.employment (iso2);
CREATE INDEX idx_others_iso2 ON cleansed.others (iso2);
CREATE INDEX idx_social_iso2 ON cleansed.social (iso2);
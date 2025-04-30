-- Создаем схемы
CREATE SCHEMA IF NOT EXISTS staging;

-- staging.iso_countries
CREATE TABLE IF NOT EXISTS staging.iso_countries(
  iso_countries_id SERIAL PRIMARY KEY,
  iso2 CHAR(2) UNIQUE NOT NULL,
  iso3 VARCHAR(3) NOT NULL,
  iso_num VARCHAR(3) NOT NULL,
  country VARCHAR(58) NOT NULL,
  country_common VARCHAR(44) NOT NULL
);

-- staging.country
CREATE TABLE IF NOT EXISTS staging.country (
    country_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    iso2 CHAR(2) NOT NULL REFERENCES staging.iso_countries(iso2),
    region VARCHAR(100),
    capital VARCHAR(100),
    population NUMERIC,
    surface_area NUMERIC,
    pop_density NUMERIC,
    pop_growth NUMERIC,
    urban_population NUMERIC,
    urban_population_growth NUMERIC,
    fertility NUMERIC,
    infant_mortality NUMERIC,
    life_expectancy_male NUMERIC,
    life_expectancy_female NUMERIC,
    sex_ratio NUMERIC,
    internet_users NUMERIC,
    co2_emissions NUMERIC,
    employment_agriculture NUMERIC,
    employment_industry NUMERIC,
    employment_services NUMERIC,
    primary_school_enrollment_male NUMERIC,
    primary_school_enrollment_female NUMERIC,
    secondary_school_enrollment_male NUMERIC,
    secondary_school_enrollment_female NUMERIC,
    post_secondary_enrollment_male NUMERIC,
    post_secondary_enrollment_female NUMERIC,
    gdp NUMERIC,
    gdp_per_capita NUMERIC,
    gdp_growth NUMERIC,
    exports NUMERIC,
    imports NUMERIC,
    refugees NUMERIC,
    threatened_species INTEGER,
    forested_area NUMERIC,
    tourists NUMERIC,
    homicide_rate NUMERIC,
    unemployment NUMERIC,
    currency_code VARCHAR(10),
    currency_name VARCHAR(50)
);

-- staging.artist
CREATE TABLE IF NOT EXISTS staging.artist (
	artist_id SERIAL PRIMARY KEY,
    mbid VARCHAR(255) UNIQUE, -- может быть NULL
    name VARCHAR(255),
    alias VARCHAR(255),
    country_id INTEGER REFERENCES staging.country(country_id),
    found_year INTEGER,
    wealth_index NUMERIC(5,2),
    crime_index NUMERIC(5,2),
    popularity_index NUMERIC(5,2),
    sex_index NUMERIC(5,2),
    performance_count INTEGER,
    scandal_index NUMERIC(5,2),
    fan_subculture VARCHAR(100),
    bio_summary TEXT,
    listeners NUMERIC,
    playcount NUMERIC,
    tags TEXT,
    url TEXT
);


-- staging.country_top_artists
CREATE TABLE IF NOT EXISTS staging.country_top_artists (
	id SERIAL PRIMARY KEY,
	mbid VARCHAR(255), -- может быть NULL
	top_artist_id INTEGER REFERENCES staging.artist(artist_id),
    country_iso2 CHAR(2),
    rank INTEGER,
    artist_name VARCHAR(255),
    playcount INTEGER,
    fetch_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXIST staging.all_countries_religion (
    acr_id SERIAL PRIMARY KEY
    iso2 varchar(2) INTEGER REFERENCES staging.country(iso2)
    region varchar(50)
    nation varchar(50)
    bahai numeric
    bahai_percent numeric
    buddhists numeric
    buddhists_percent numeric
    chinese_folk numeric
    chinese_folk_percent numeric
    christians numeric
    christians_percent numeric
    confucianist numeric
    confucianist_percent numeric
    daoist numeric
    daoist_percent numeric
    ethnic_religionist numeric
    ethnic_religionist_percent numeric
    hindus numeric
    hindus_percent numeric
    jews numeric
    jews_percent numeric
    muslims numeric
    muslims_percent numeric
    non_religious numeric
    non_religious_percent numeric
    sikhs numeric
    sikhs_percent numeric
)

--не то чтобы она нужна, но на всякий
CREATE TABLE IF NOT EXIST staging.ihme_gbd (
    measure_name varchar(50)
    location_id numeric
    location_name varchar(50)
    cause_name varchar(50)
    "year" numeric
    val numeric
    upper numeric
    lower numeric
    iso3 varchar
    iso2 varchar
)

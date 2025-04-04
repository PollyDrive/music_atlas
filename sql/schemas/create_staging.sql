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
-- staging.country_top_artists
CREATE TABLE IF NOT EXISTS staging.country_top_artists (
	id SERIAL PRIMARY KEY,
	mbid VARCHAR(255), -- может быть NULL
	top_artist_id INTEGER REFERENCES staging.artist(artist_id), -- суррогатная ссылка
    country_iso2 CHAR(2),
    rank INTEGER,
    artist_name VARCHAR(255),
    playcount INTEGER,
    fetch_date DATE DEFAULT CURRENT_DATE,
    UNIQUE (country_iso2, top_artist_id, fetch_date),
    CONSTRAINT unique_cta_entry UNIQUE (country_iso2, mbid, fetch_date)
);

-- staging.artist
CREATE TABLE staging.artist (
	artist_id SERIAL PRIMARY KEY,
    mbid VARCHAR(255) UNIQUE, -- может быть NULL
    name VARCHAR(255),
    alias VARCHAR(255),
    country_id INTEGER REFERENCES staging.country(country_id),
    birth_year INTEGER,
    found_year INTEGER,
    wealth_index NUMERIC(5,2),
    crime_index NUMERIC(5,2),
    popularity_index NUMERIC(5,2),
    sex_index NUMERIC(5,2),
    performance_count INTEGER,
    scandal_index NUMERIC(5,2),
    fan_subculture VARCHAR(100)
);

-- staging.genre
CREATE TABLE IF NOT EXISTS staging.genre (
    genre_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    subgenre VARCHAR(100),
    origin_country VARCHAR(100),
    origin_year INTEGER
);

-- staging.album
CREATE TABLE IF NOT EXISTS staging.album (
    album_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist_id INTEGER REFERENCES staging.artist(artist_id),
    release_year INTEGER,
    label VARCHAR(100),
    popularity_index NUMERIC(5,2),
    re_release_count INTEGER
);

-- staging.song
CREATE TABLE IF NOT EXISTS staging.song (
    song_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist_id INTEGER REFERENCES staging.artist(artist_id),
    genre_id INTEGER REFERENCES staging.genre(genre_id),
    album_id INTEGER REFERENCES staging.album(album_id),
    country_id INTEGER REFERENCES staging.country(country_id),
    year INTEGER,
    lyrics TEXT,
    bpm INTEGER,
    duration_sec INTEGER,
    explicit BOOLEAN,
    popularity_index NUMERIC(5,2),
    sentiment_score NUMERIC(5,2),
    philosophy_score NUMERIC(5,2),
    meme_potential NUMERIC(5,2),
    depression_score NUMERIC(5,2),
    sex_potential NUMERIC(5,2),
    protest_index NUMERIC(5,2),
    alcohol_mentions_count INTEGER,
    drug_mentions_count INTEGER,
    dominant_listener_gender VARCHAR(50)
);

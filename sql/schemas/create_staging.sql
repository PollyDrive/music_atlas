-- Создаем схемы
CREATE SCHEMA IF NOT EXISTS staging;

-- staging.country
CREATE TABLE staging.country (
    country_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    economic_system VARCHAR(100),
    suicide_rate NUMERIC(5,2),
    major_religion VARCHAR(100),
    birth_rate NUMERIC(5,2),
    divorce_rate NUMERIC(5,2)
);

-- staging.genre
CREATE TABLE staging.genre (
    genre_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    subgenre VARCHAR(100),
    origin_country VARCHAR(100),
    origin_year INTEGER
);

-- staging.artist
CREATE TABLE staging.artist (
    artist_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
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

-- staging.album
CREATE TABLE staging.album (
    album_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist_id INTEGER REFERENCES staging.artist(artist_id),
    release_year INTEGER,
    label VARCHAR(100),
    popularity_index NUMERIC(5,2),
    re_release_count INTEGER
);

-- staging.song
CREATE TABLE staging.song (
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

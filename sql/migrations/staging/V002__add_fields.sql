ALTER TABLE staging.artist
ADD COLUMN country_code CHAR(2),
ADD COLUMN birth_year INTEGER,
ADD COLUMN death_year INTEGER,
ADD COLUMN gender VARCHAR(50),
ADD COLUMN disambiguation TEXT,
ADD COLUMN type VARCHAR(100);

ALTER TABLE staging.country_top_artists
ALTER COLUMN playcount TYPE NUMERIC;

ALTER TABLE staging.country
    ADD COLUMN IF NOT EXISTS majority_religion TEXT,
    ADD COLUMN IF NOT EXISTS languages         TEXT,
    ADD COLUMN IF NOT EXISTS suicide_rate_2021 NUMERIC,
    ADD COLUMN IF NOT EXISTS press_freedom_2024 NUMERIC,
    ADD COLUMN IF NOT EXISTS depression_rate_2021 NUMERIC,
    ADD COLUMN IF NOT EXISTS alcohol_per_capita_2019   NUMERIC,
    ADD COLUMN IF NOT EXISTS iso3 CHAR(3);

UPDATE staging.country AS c
SET    iso3 = ic.iso3
FROM   staging.iso_countries AS ic
WHERE  c.iso2 = ic.iso2
  AND  (c.iso3 IS NULL OR c.iso3 = '');
ALTER TABLE staging.country
    ADD COLUMN IF NOT EXISTS majority_religion TEXT,
    ADD COLUMN IF NOT EXISTS languages         TEXT,
    ADD COLUMN IF NOT EXISTS suicide_rate_2021 NUMERIC,
    ADD COLUMN IF NOT EXISTS press_freedom_2024 NUMERIC,
    ADD COLUMN IF NOT EXISTS hdi_2022          NUMERIC,
    ADD COLUMN IF NOT EXISTS depression_rate_2021 NUMERIC,
    ADD COLUMN IF NOT EXISTS median_age_2022   NUMERIC,
    -- ADD COLUMN IF NOT EXISTS top_social_network TEXT;


ALTER TABLE staging.country
    ADD COLUMN IF NOT EXISTS iso3 CHAR(3);

UPDATE staging.country AS c
SET    iso3 = ic.iso3
FROM   staging.iso_countries AS ic
WHERE  c.iso2 = ic.iso2
  AND  (c.iso3 IS NULL OR c.iso3 = '');
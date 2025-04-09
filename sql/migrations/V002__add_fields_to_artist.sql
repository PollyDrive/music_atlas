ALTER TABLE staging.artist
ADD COLUMN country_code CHAR(2),
ADD COLUMN birth_year INTEGER,
ADD COLUMN death_year INTEGER,
ADD COLUMN gender VARCHAR(50),
ADD COLUMN disambiguation TEXT,
ADD COLUMN type VARCHAR(100);

ALTER TABLE staging.country_top_artists
ALTER COLUMN playcount TYPE BIGINT;

-- ALTER TABLE staging.artist
-- DROP COLUMN IF EXISTS found_year,
-- DROP COLUMN IF EXISTS wealth_index,
-- DROP COLUMN IF EXISTS crime_index,
-- DROP COLUMN IF EXISTS popularity_index,
-- DROP COLUMN IF EXISTS sex_index,
-- DROP COLUMN IF EXISTS performance_count,
-- DROP COLUMN IF EXISTS scandal_index,
-- DROP COLUMN IF EXISTS fan_subculture;
CREATE SCHEMA IF NOT EXISTS cleansed;

CREATE TABLE IF NOT EXISTS cleansed.top_10_artist(
    iso2 char(2) REFERENCES cleansed.country(iso2),
    rank numeric,
    artist_name char(50),
    PRIMARY KEY (country_iso2, rank)
)

CREATE TABLE IF NOT EXISTS cleansed.artist(
    name char(60),
    alias char(60),
    bio_summary TEXT,
    listeners INT,
    country_code char(3),
    gender CHAR(15),
    disambiguation TEXT,
    PRIMARY KEY (name)
)
insert into cleansed.artist
SELECT
    name,
    alias,
    bio_summary,
    listeners,
    country_code,
    gender,
    disambiguation
from staging.artist

---сначала дропаем дубликаты
DELETE FROM staging.country_top_artists a
USING (
  SELECT MIN(ctid) as keep_ctid, rank, country_iso2, artist_name
  FROM staging.country_top_artists
  GROUP BY rank, country_iso2, artist_name
  HAVING COUNT(*) > 1
) dup
WHERE a.rank = dup.rank
  AND a.country_iso2 = dup.country_iso2
  AND a.artist_name = dup.artist_name
  AND a.ctid <> dup.keep_ctid;

insert into cleansed.top_10_artist 
SELECT
    cta_id,
    country_iso2,
    rank,
    artist_name
FROM staging.country_top_artists
WHERE rank <=10

----------------------------------------------

ALTER TABLE cleansed.artist_tag
ADD CONSTRAINT fk_artist_name
FOREIGN KEY (name) REFERENCES cleansed.top_10_artist(artist_name);

ALTER TABLE cleansed.top_10_artist
ADD CONSTRAINT fk_top_10_artist_country
FOREIGN KEY (iso2) REFERENCES cleansed.country(country_iso2);

ALTER TABLE cleansed.top_10_artist
ADD CONSTRAINT fk_top_10_artist_name
FOREIGN KEY (artist_name) REFERENCES cleansed.artist(name);

ALTER TABLE cleansed.artist_tag
ADD CONSTRAINT fk_art_tag_name_art_name
FOREIGN KEY (name) REFERENCES cleansed.artist(name);

----------------------------------------------
CREATE TABLE IF NOT EXISTS cleansed.tag_info (
    tag TEXT PRIMARY KEY,
    description TEXT,
    reach INT,
    taggings INT,
    fetch_date DATE
);

CREATE TABLE IF NOT EXISTS cleansed.artist_tag(
    artist_id INT,
    name TEXT,
    tag TEXT,
    source TEXT,
    fetch_date DATE,
    PRIMARY KEY (artist_id, tag)
)

ALTER TABLE cleansed.artist_tag
ADD CONSTRAINT fk_artist_tag_info
FOREIGN KEY (tag) REFERENCES cleansed.tag_info(tag);

-- bahai_percent, buddhist_percent, chinese_folk_percent, christians_percent, confucianist_percent, daoist_percent, ethnic_religionist_percent, hindus_percent, jews_percent, non_religious_percent, muslims_percent, sikhs_percent
-- bahai, buddhist, chinese_folk, christians, confucianist, daoist, ethnic_religionist, hindus, jews, non_religious, muslims, sikhs

CREATE TABLE cleansed.nation_top_religions (
    nation PRIMARY KEY VARCHAR(255),
    iso2 CHAR(2),
    first_popular_religion VARCHAR(255),
    first_percent DECIMAL(5,2),
    second_popular_religion VARCHAR(255),
    second_percent DECIMAL(5,2),
    third_popular_religion VARCHAR(255),
    third_percent DECIMAL(5,2)
);

-- выяснилось, что нехватает стран для FK
insert into cleansed.country
select iso2, nation, region
from staging.all_countries_religion
where iso2 not in (
	select iso2
	from cleansed.country
);

ALTER TABLE cleansed.nation_top_religions
ADD CONSTRAINT fk_religions_country
FOREIGN KEY (iso2) REFERENCES cleansed.country(iso2);

ALTER TABLE cleansed.life_value
drop column region;

ALTER TABLE cleansed.gdp
drop column region;

ALTER TABLE cleansed.education
drop column region;

ALTER TABLE cleansed.population
drop column region;

ALTER TABLE cleansed.employment
drop column region;

ALTER TABLE cleansed.others
drop column region;

ALTER TABLE cleansed.social
drop column region;
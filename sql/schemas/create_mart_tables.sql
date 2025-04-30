-- mart.life_exp_male_post_sec_enroll_male_top

-- 1. Отбираем 5 стран с высокими life_expectancy_male и post_secondary_enrollment_male
WITH top_countries AS (
  SELECT iso2, e.name AS country_name
  FROM cleansed.life_value lv
  JOIN cleansed.education e USING (iso2) 
  where lv.life_expectancy_male is not null and e.post_secondary_enrollment_male is not null
  ORDER BY lv.life_expectancy_male DESC, e.post_secondary_enrollment_male DESC
  limit 5
),

-- 2. Находим артистов из этих стран (топ-5)
top_artists AS (
  SELECT DISTINCT
    cta.artist_name,
    cta.rank,
    tc.iso2,
    tc.country_name
  FROM top_countries tc
  JOIN staging.country_top_artists cta ON cta.country_iso2 = tc.iso2
  where cta.rank <=5
),

-- 3. Находим жанры этих артистов
artist_genres AS (
  SELECT
    at.tag,
    at.name AS artist_name,
    ta.country_name,
    ta.rank,
    ta.iso2
  FROM top_artists ta
  JOIN cleansed.artist_tag at ON at.name = ta.artist_name
)

-- 4. Считаем частоту по артистам и стране
insert into mart.life_exp_male_post_sec_enroll_male_top
select
  country_name,
  artist_name,
  rank, 
  tag
FROM artist_genres
GROUP BY country_name, artist_name, rank, tag
ORDER BY country_name desc, rank asc;
------------------------------------------------------------

-- 1. Получаем Топ-5 стран по параметру 1
WITH top_first AS (
  SELECT iso2
  FROM cleansed.population p 
  WHERE pop_density IS NOT NULL
  ORDER BY pop_density DESC
  LIMIT 10
),

-- 2. Получаем Топ-5 стран по параметру 2
top_sec AS (
  SELECT iso2
  FROM cleansed.employment em
  WHERE employment_services IS NOT NULL
  ORDER BY employment_services DESC
  LIMIT 10
),

-- 2. Получаем Топ-5 стран по параметру 3
top_third AS (
  SELECT iso2
  FROM cleansed.others
  WHERE homicide_rate IS NOT NULL
  ORDER BY homicide_rate DESC
  LIMIT 10
),

-- 3. Пересечение: страны, попавшие во все топы
top_countries AS (
  SELECT lv.iso2, lv.name AS country_name
  FROM cleansed.life_value lv
  WHERE iso2 IN (
    SELECT iso2 FROM top_first
    INTERSECT
    SELECT iso2 FROM top_sec
    INTERSECT
    SELECT iso2 FROM top_third
  )
),

-- 4. Топ-артисты этих стран (по рангу)
top_artists AS (
  SELECT DISTINCT
    cta.artist_name,
    cta.rank,
    tc.iso2,
    tc.country_name
  FROM top_countries tc
  JOIN staging.country_top_artists cta ON cta.country_iso2 = tc.iso2
  WHERE cta.rank <= 3
),

-- 5. Жанры этих артистов
artist_genres AS (
  SELECT
    at.tag,
    at.name AS artist_name,
    ta.country_name,
    ta.rank,
    ta.iso2
  FROM top_artists ta
  JOIN cleansed.artist_tag at ON at.name = ta.artist_name
)

-- 6. Финальный вывод: какие теги встречаются по странам
SELECT
  country_name,
  artist_name,
  rank
FROM artist_genres
ORDER BY country_name DESC, rank ASC;

--------------------------------------------------------------------------------
-- 1. Получаем Топ-5 стран по параметру 1
WITH top_first AS (
  SELECT iso2
  FROM cleansed.education em
  WHERE post_secondary_enrollment_male IS NOT NULL
  ORDER BY post_secondary_enrollment_male DESC
  LIMIT 15
),
-- 2. Получаем Топ-5 стран по параметру 2
top_sec AS (
  SELECT iso2
  FROM cleansed.life_value em
  WHERE life_expectancy_female IS NOT NULL
  ORDER BY life_expectancy_female DESC
  LIMIT 10
),
-- 2. Получаем Топ-5 стран по параметру 3
-- top_third AS (
--   SELECT iso2
--   FROM cleansed.others
--   WHERE homicide_rate IS NOT NULL
--   ORDER BY homicide_rate DESC
--   LIMIT 15
-- ),
-- 3. Пересечение: страны, попавшие во все топы
top_countries AS (
  SELECT lv.iso2, lv.name AS country_name
  FROM cleansed.life_value lv
  WHERE iso2 IN (
    SELECT iso2 FROM top_first
    INTERSECT
    SELECT iso2 FROM top_sec
    -- INTERSECT
    -- SELECT iso2 FROM top_third
  )
),
-- 4. Топ-артисты этих стран (по рангу)
top_artists AS (
  SELECT DISTINCT
    cta.artist_name,
    cta.rank,
    tc.iso2,
    tc.country_name
  FROM top_countries tc
  JOIN staging.country_top_artists cta ON cta.country_iso2 = tc.iso2
  WHERE cta.rank <= 3
),
-- 5. Жанры этих артистов
artist_genres AS (
  SELECT
    at.tag,
    at.name AS artist_name,
    ta.country_name,
    ta.rank,
    ta.iso2
  FROM top_artists ta
  JOIN cleansed.artist_tag at ON at.name = ta.artist_name
)
-- 6. Финальный вывод: какие теги встречаются по странам
SELECT
  country_name,
  artist_name,
  rank,
  tag
FROM artist_genres
ORDER BY country_name DESC, rank ASC;

insert into mart.emp_services_homicide_top
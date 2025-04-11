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


-- 1. Отбираем 5 стран с нужными характеристиками
WITH top_countries AS (
  SELECT iso2, p.name AS country_name
  FROM cleansed.population p
  JOIN cleansed.employment e USING (iso2)
  JOIN cleansed.others o USING (iso2) 
  where p.pop_density is not null and e.employment_services is not null and o.homicide_rate is not null
  ORDER BY o.homicide_rate desc, p.pop_density DESC, e.employment_services desc 
  limit 5
),

-- 2. Находим артистов из этих стран (топ-артисты)
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
insert into mart.homicide_density_services_top
select
  country_name,
  artist_name,
  rank, 
  tag
FROM artist_genres
GROUP BY country_name, artist_name, rank, tag
ORDER BY country_name desc, rank asc;





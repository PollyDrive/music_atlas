ALTER TABLE staging.country
    ADD COLUMN IF NOT EXISTS majority_religion TEXT,
    ADD COLUMN IF NOT EXISTS languages         TEXT,
    ADD COLUMN IF NOT EXISTS suicide_rate_2021 NUMERIC,
    ADD COLUMN IF NOT EXISTS press_freedom_2024 NUMERIC,
    ADD COLUMN IF NOT EXISTS depression_rate_2021 NUMERIC,
    ADD COLUMN IF NOT EXISTS alcohol_per_capita_2019   NUMERIC,



ALTER TABLE staging.country
    ADD COLUMN IF NOT EXISTS iso3 CHAR(3);

UPDATE staging.country AS c
SET    iso3 = ic.iso3
FROM   staging.iso_countries AS ic
WHERE  c.iso2 = ic.iso2
  AND  (c.iso3 IS NULL OR c.iso3 = '');

ALTER TABLE public.dataset_bahai RENAME COLUMN "% Baha'is(2020)1 [X]" TO bahai_percent;
ALTER TABLE public.dataset_buddhists RENAME COLUMN "% Buddhist(2020)1 [X]" TO buddhists_percent;
ALTER TABLE public.dataset_chinese_folk RENAME COLUMN "% Chinese folk(2020)1 [X]" TO chinese_folk-religionists_percent;
ALTER TABLE public.dataset_christians RENAME COLUMN bahai_percent TO christians_percent;
ALTER TABLE public.dataset_confucianists RENAME COLUMN bahai_percent TO confucianist_percent;
ALTER TABLE public.dataset_daoist RENAME COLUMN bahai_percent TO daoist_percent;
ALTER TABLE public.dataset_ethnic_religionist RENAME COLUMN "% Ethnic religionists(2020)1 [X]" TO ethnic_religionist_percent;
ALTER TABLE public.dataset_hindus RENAME COLUMN "% Hindus(2020)1 [X]" TO hindus_percent;
ALTER TABLE public.dataset_jews RENAME COLUMN "% Jews(2020)1 [X]" TO jews_percent;
ALTER TABLE public.dataset_muslims RENAME COLUMN "% Muslims(2020)1 [X]" TO muslims_percent;  
ALTER TABLE public.dataset_non_religious RENAME COLUMN "% Non-Religious(2020)1 [X]" TO non_religious_percent;  
ALTER TABLE public.dataset_sikhs RENAME COLUMN "% Sikhs(2020)1 [X]" TO sikhs_percent;  

ALTER TABLE public.dataset_bahai RENAME COLUMN "REGION" TO region;
ALTER TABLE public.dataset_buddhists RENAME COLUMN "REGION" TO region;
ALTER TABLE public.dataset_chinese_folk RENAME COLUMN "REGION" TO region;
ALTER TABLE public.dataset_christians RENAME COLUMN "REGION" TO region;
ALTER TABLE public.dataset_confucianists RENAME COLUMN "REGION" TO region;
ALTER TABLE public.dataset_daoist RENAME COLUMN "REGION" TO region;
ALTER TABLE public.dataset_ethnic_religionist RENAME COLUMN "REGION" TO region;
ALTER TABLE public.dataset_hindus RENAME COLUMN "REGION" TO region;
ALTER TABLE public.dataset_jews RENAME COLUMN "REGION" TO region;
ALTER TABLE public.dataset_muslims RENAME COLUMN "REGION" TO region;
ALTER TABLE public.dataset_non_religious RENAME COLUMN "REGION" TO region;
ALTER TABLE public.dataset_sikhs RENAME COLUMN "REGION" TO region;

-- это были в отчаянии скачанные 12 csv на каждую религию, потому что искать рабочее апи я уже не могу.
-- Надеюсь, мне никогда не придется снова их переименовывать
CREATE TABLE IF NOT EXISTS staging.all_countries_religion as
SELECT * FROM public.dataset_bahai
join public.dataset_buddhists USING(nation, region)
join public.dataset_chinese_folk USING(nation, region)
join public.dataset_christians USING(nation, region)
join public.dataset_confucianists USING(nation, region)
join public.dataset_daoist USING(nation, region)
join public.dataset_ethnic_religionist USING(nation, region)
join public.dataset_hindus USING(nation, region)
join public.dataset_jews USING(nation, region)
join public.dataset_muslims USING(nation, region)
join public.dataset_non_religious USING(nation, region)
join public.dataset_sikhs USING(nation, region)

join staging.iso_countries on public.dataset_sikhs.nation = staging.iso_countries
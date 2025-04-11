drop table if exists mart.life_exp_male_post_sec_enroll_male_top
drop table if exists mart.homicide_density_services_top

CREATE TABLE mart.life_exp_male_post_sec_enroll_male_top (
	country_name VARCHAR(50),
    artist_name VARCHAR(50),
    rank INTEGER
)

CREATE TABLE mart.homicide_density_services_top (
	country_name VARCHAR(50),
    artist_name VARCHAR(50),
    rank INTEGER,
    tag VARCHAR(100)
)

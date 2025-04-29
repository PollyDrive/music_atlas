CREATE SCHEMA IF NOT EXISTS cleansed;

CREATE TABLE IF NOT EXISTS cleansed.tag_info (
    tag TEXT PRIMARY KEY,
    description TEXT,
    reach INT,
    taggings INT,
    fetch_date DATE DEFAULT CURRENT_DATE
);

--Сделать: country_language

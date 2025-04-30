-- CREATE INDEX idx_country_data_iso2 ON cleansed.country_data (iso2);
CREATE INDEX idx_depression_iso2 ON cleansed.life_value (iso2);
CREATE INDEX idx_population_iso2 ON cleansed.population (iso2);
CREATE INDEX idx_gdp_iso2 ON cleansed.gdp (iso2);
CREATE INDEX idx_education_iso2 ON cleansed.education (iso2);
CREATE INDEX idx_employment_iso2 ON cleansed.employment (iso2);
CREATE INDEX idx_others_iso2 ON cleansed.others (iso2);
CREATE INDEX idx_social_iso2 ON cleansed.social (iso2);
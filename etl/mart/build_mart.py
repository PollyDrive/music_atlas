from etl.mart.analyze_quadrant import analyze_quadrant_artist_tag
from etl.mart.analyze_quadrant import analyze_single_indicator
from etl.mart.analyze_with_religion import analyze_religion_vs_indicator

# уже запущено
# analyze_quadrant_artist_tag('social', 'alcohol_per_capita_2019', 'social', 'depression_rate_2021', 10)
# analyze_quadrant_artist_tag('employment', 'unemployment', 'education', 'post_secondary_enrollment_female', 10)
# analyze_quadrant_artist_tag('employment', 'unemployment', 'social', 'suicide_rate_2021', 5)
# analyze_quadrant_artist_tag('population', 'sex_ratio', 'gdp', 'gdp_per_capita', 5)
# analyze_quadrant_artist_tag('life_value', 'life_expectancy_male', 'social', 'alcohol_per_capita_2019', 5)

# analyze_single_indicator('social', 'press_freedom_2024', 5)
# analyze_single_indicator('life_value', 'infant_mortality', 5)

# --todo--
# объединить две ф в одну

# пока хз что с этим делать
# analyze_quadrant_artist_tag('social', 'press_freedom_2024', 'population', 'refugees', 5)
# analyze_quadrant_artist_tag('employment', 'employment_industry', 'population', 'urban_population', 5)


# analyze_religion_vs_indicator('employment', 'unemployment', 'first', 10, False)
analyze_religion_vs_indicator('population', 'sex_ratio', 'first', 10, False)
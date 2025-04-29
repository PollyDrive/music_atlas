-- -- seed_test_data.sql
-- -- Минимальные тестовые данные для проверки связей

-- -- Жанры
-- INSERT INTO staging.genre (name, subgenre, origin_country, origin_year)
-- VALUES
-- ('Rock', 'Alternative', 'USA', 1965),
-- ('Techno', 'Detroit Techno', 'USA', 1980);

-- -- Артисты
-- INSERT INTO staging.artist (name, country_id, birth_year, wealth_index, crime_index, popularity_index, sex_index, performance_count, scandal_index, fan_subculture)
-- VALUES
-- ('The Rolling Stones', 1, 1962, 85.0, 5.0, 95.0, 70.0, 1500, 8.0, 'Rockers'),
-- ('Kraftwerk', 2, 1970, 65.0, 2.0, 80.0, 20.0, 500, 1.0, 'Techno-heads');

-- -- Альбомы
-- INSERT INTO staging.album (title, artist_id, release_year, label, popularity_index, re_release_count)
-- VALUES
-- ('Sticky Fingers', 1, 1971, 'Rolling Stones Records', 90.0, 3),
-- ('Autobahn', 2, 1974, 'Philips', 75.0, 1);

-- -- Песни
-- INSERT INTO staging.song (title, artist_id, genre_id, album_id, country_id, year, lyrics, bpm, duration_sec, explicit, popularity_index, sentiment_score, philosophy_score, meme_potential, depression_score, sex_potential, protest_index, alcohol_mentions_count, drug_mentions_count, dominant_listener_gender)
-- VALUES
-- ('Brown Sugar', 1, 1, 1, 1, 1971, 'Gold coast slave ship bound for cotton fields...', 132, 225, true, 95.0, -0.2, 0.5, 0.7, 0.3, 0.8, 0.1, 3, 5, 'mixed'),
-- ('Autobahn', 2, 2, 2, 2, 1974, 'Wir fahren, fahren, fahren auf der Autobahn...', 125, 270, false, 80.0, 0.1, 0.6, 0.4, 0.1, 0.3, 0.0, 0, 0,'mixed');

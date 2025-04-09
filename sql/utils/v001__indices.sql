CREATE INDEX idx_song_artist_id ON staging.song(artist_id);
CREATE INDEX idx_song_genre_id ON staging.song(genre_id);
CREATE INDEX idx_album_artist_id ON staging.album(artist_id);
CREATE INDEX idx_artist_country_id ON staging.artist(country_id);
CREATE INDEX idx_iso_countries_iso2 ON staging.iso_countries(iso2);
CREATE INDEX idx_country_iso2 ON staging.country(iso2);
-- CREATE INDEX idx_album_country_id ON staging.album(country_id);
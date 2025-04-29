CREATE INDEX idx_artist_mbid ON staging.artist(mbid);
CREATE UNIQUE INDEX unique_cta_entry
    ON staging.country_top_artists(country_iso2, mbid, fetch_date);

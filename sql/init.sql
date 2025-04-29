-- -- init.sql

\echo '==> Resetting database...'
\i '/docker-entrypoint-initdb.d/utils/dev_reset.sql'

\echo '==> Creating staging schema and tables...'
\i '/docker-entrypoint-initdb.d/migrations/staging/v001__create_staging.sql'

\echo '==> Creating indices...'
\i '/docker-entrypoint-initdb.d/utils/v001__indices.sql'

-----------------

-- \echo '==> Loading data...'
-- \echo '==> Creating iso-countries'
\i '/docker-entrypoint-initdb.d/schemas/iso_countries.sql'
\i '/docker-entrypoint-initdb.d/migrations/staging/V002__add_fields.sql'
\i '/docker-entrypoint-initdb.d/migrations/staging/v003__create_indices.sql'
\i '/docker-entrypoint-initdb.d/migrations/staging/v004__create_enrich.sql'

-- \i '/docker-entrypoint-initdb.d/migrations/v004__cleansed_tag_info.sql'
-- \i '/docker-entrypoint-initdb.d/migrations/v006__add_to_countries.sql'



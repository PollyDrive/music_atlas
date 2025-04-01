-- -- init.sql

\echo '==> Resetting database...'
\i '/docker-entrypoint-initdb.d/utils/dev_reset.sql'

\echo '==> Creating staging schema and tables...'
\i '/docker-entrypoint-initdb.d/schemas/create_staging.sql'

\echo '==> Creating indices...'
\i '/docker-entrypoint-initdb.d/schemas/indices.sql'

\echo '==> Seeding staging tables...'
\i '/docker-entrypoint-initdb.d/seeds/seed_test_data.sql'

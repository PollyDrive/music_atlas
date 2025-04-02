-- -- Add sex_ratio column to staging.country table
-- -- This migration adds a missing column that is needed by the ETL process

-- -- Start a transaction
-- BEGIN;

-- -- Add the sex_ratio column as NUMERIC type
-- ALTER TABLE staging.country 
-- ADD COLUMN sex_ratio NUMERIC;

-- -- Add a comment explaining the column's purpose
-- COMMENT ON COLUMN staging.country.sex_ratio IS 'Ratio of males to females (males per 100 females)';

-- -- Commit the transaction
-- COMMIT;


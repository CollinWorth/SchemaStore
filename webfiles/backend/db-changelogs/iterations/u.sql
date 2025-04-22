
-- chageset austin:1
-- add timestamp to orders table
BEGIN;
ALTER TABLE orders
   ADD COLUMN created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
COMMIT;

-- changeset austin:2
-- change img in products to text type
BEGIN;
ALTER TABLE products
   ALTER COLUMN img TYPE TEXT;
COMMIT;

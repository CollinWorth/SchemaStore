-- changeset austin:2
-- change img in products to text type
BEGIN;
ALTER TABLE products
   ALTER COLUMN img TYPE TEXT;
COMMIT;
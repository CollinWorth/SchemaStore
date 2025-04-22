
-- chageset austin:1
-- add timestamp to orders table
BEGIN;
ALTER TABLE orders
   ADD COLUMN created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
COMMIT;
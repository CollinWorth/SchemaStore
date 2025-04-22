
-- changeset austin:1
-- add user roles
BEGIN;
INSERT INTO roles(user_role) VALUES
   ('admin'),
   ('buyer'),
   ('seller');
COMMIT;

-- changeset austin:2
-- add first admin user
BEGIN;
INSERT INTO users (username, password, email, role_id)
   VALUES ('admin', 'tail', 'admin@idontexist.com', 1);
COMMIT;

-- changeset austin:3
-- add order number to orders table
BEGIN;
ALTER TABLE orders
   DROP CONSTRAINT product_orders_pkey,
   DROP COLUMN product_sku,
   DROP COLUMN amount,
   ADD COLUMN id SERIAL PRIMARY KEY;

CREATE TABLE ordered_items (
   order_id INT NOT NULL,
   product_sku TEXT NOT NULL,
   amount INT NOT NULL,
   FOREIGN KEY (order_id) REFERENCES orders(id)
);
COMMIT;

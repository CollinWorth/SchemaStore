-- liquibase formatted sql

-- changeset austin:1
BEGIN;

ALTER TABLE user_roles
   RENAME TO roles;

ALTER TABLE product_orders
   RENAME TO orders;

COMMIT;

-- changeset austin:2
BEGIN;

-- First remove the foreign key in products
ALTER TABLE products
   DROP CONSTRAINT products_category_fkey,
   DROP category;

-- Next give categories an id
ALTER TABLE categories
   ADD COLUMN id SERIAL,
   DROP CONSTRAINT categories_pkey,
   ADD CONSTRAINT categories_pkey PRIMARY KEY (id);

-- Finally add relation between products and categories
CREATE TABLE products_categories (
   product_sku TEXT,
   category_id INT,

   FOREIGN KEY (product_sku) REFERENCES products(sku)
      ON UPDATE CASCADE
      ON DELETE NO ACTION,
   FOREIGN KEY (category_id) REFERENCES categories(id)
      ON UPDATE CASCADE
      ON DELETE NO ACTION,
   PRIMARY KEY (product_sku, category_id)
);

COMMIT;

-- changeset austin:3
BEGIN;

-- First delete the foreign key in users
ALTER TABLE "users"
   DROP CONSTRAINT "users_role_fkey",
   DROP COLUMN "role";

-- Alter the user_roles table to include an id
ALTER TABLE "roles"
   DROP CONSTRAINT "user_roles_pkey",
   ADD COLUMN id SERIAL,
   ADD CONSTRAINT "roles_pkey" PRIMARY KEY (id);

-- Add foreign key back to users
ALTER TABLE "users"
   ADD COLUMN "role_id" INT,
   ADD CONSTRAINT "users_role_fkey"
      FOREIGN KEY ("role_id") REFERENCES "roles"(id)
         ON UPDATE CASCADE
         ON DELETE NO ACTION;

COMMIT;

-- changeset austin:4
-- Add image column to products table
BEGIN;

ALTER TABLE "products"
   ADD COLUMN "img" BYTEA;

COMMIT;

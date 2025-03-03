-- liquibase formatted sql

-- changeset austin: 4
ALTER TABLE products
ADD CONSTRAINT positive_stock CHECK (stock >= 0);
-- rollback
ALTER TABLE products
DROP CONSTRAINT positive_stock;

-- changeset austin: 3
ALTER TABLE products
ADD CONSTRAINT positive_price CHECK (price >= 0);
-- rollback
ALTER TABLE products
DROP CONSTRAINT postiive_price;

-- changeset austin:2
ALTER TABLE products
ADD CONSTRAINT fk_categories
FOREIGN KEY (category) REFERENCES categories(category);
--rollback
ALTER TABLE products
DROP CONSTRAINT tk_categories;

-- ChangeSet: collins #1 (create)
CREATE TABLE products (
    sku TEXT PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL
);

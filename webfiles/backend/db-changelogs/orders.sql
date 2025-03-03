-- liquibase formatted sql

-- changeset: austin 1
CREATE TABLE product_orders (
  FOREIGN KEY username REFERENCES users(username),
  FOREIGN KEY product_sku REFERENCES products(sku),
  amount INT,
  ship_addr TEXT NOT NULL,
  total DECIMAL(100, 2),

  PRIMARY KEY (username, product_sku),
  CHECK (amount > 0),
  CHECK (total >= 0)
);
-- rollback
DROP TABLE product_orders;
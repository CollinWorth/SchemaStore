-- liquibase formated sql

-- changeset: austin 1
CREATE TABLE reserved_items (
  FOREIGN KEY (username) REFERENCES users(username),
  FOREIGN KEY (product_sku) REFERENCES products(sku),
  amount INT,

  PRIMARY KEY (username, product_sku),
  CHECK (amount > 0)
);
-- rollback
DROP TABLE reserved_items;
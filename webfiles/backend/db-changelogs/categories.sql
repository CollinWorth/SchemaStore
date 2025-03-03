--liquibase formatted sql

-- changeset austin:1 (create)
CREATE TABLE categories (
  category VARCHAR(50) PRIMARY KEY
);
-- rollback
DROP TABLE categories;
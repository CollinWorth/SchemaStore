-- liquibase formatted sql

-- changeset: austin 1 (create)
CREATE TABLE user_roles (
  user_role VARCHAR(50) PRIMARY KEY;
)
-- liquibase formatted sql

-- changeset: austin 2 (create)
ALTER TABLE users
ADD CONSTRAINT fk_roles
FOREIGN KEY (user_role) REFERENCES user_roles(user_role);

-- ChangeSet: collins #1 (create)
CREATE TABLE users (
    username VARCHAR(50) PRIMARY KEY NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password TEXT NOT NULL
);

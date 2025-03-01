-- ChangeSet: collins #2 (create)
CREATE TABLE products (
    sku TEXT PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL
);
-- liquibase formatted sql

-- changeset austin:1
CREATE TABLE user_roles (
  user_role VARCHAR(20) PRIMARY KEY
);

-- changeset austin:2
CREATE TABLE categories (
  category VARCHAR(20) PRIMARY KEY
);

-- changeset austin:3
CREATE TABLE users (
  username VARCHAR(20) PRIMARY KEY,
  email VARCHAR(50) UNIQUE NOT NULL,
  password VARCHAR(50) NOT NULL,
  role VARCHAR(20),

  FOREIGN KEY (role) REFERENCES user_roles(user_role)
);

-- changeset austin:4
CREATE TABLE products (
  sku TEXT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  price DECIMAL(10, 2) NOT NULL,
  stock INT NOT NULL,
  category VARCHAR(20),

  FOREIGN KEY (category) REFERENCES categories(category),
  CHECK (price >= 0),
  CHECK (stock >= 0)
);

-- changeset austin:5
CREATE TABLE reserved_items (
  username TEXT,
  product_sku TEXT,
  amount INT,

  FOREIGN KEY (username) REFERENCES users(username),
  FOREIGN KEY (product_sku) REFERENCES products(sku),
  PRIMARY KEY (username, product_sku),
  CHECK (amount > 0)
);

-- changeset austin:6
CREATE TABLE product_orders (
  username TEXT,
  product_sku TEXT,
  amount INT,
  ship_addr TEXT NOT NULL,
  total DECIMAL(100, 2),

  PRIMARY KEY (username, product_sku),
  FOREIGN KEY (username) REFERENCES users(username),
  FOREIGN KEY (product_sku) REFERENCES products(sku),
  CHECK (amount > 0),
  CHECK (total >= 0)
);

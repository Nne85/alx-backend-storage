-- creates a table users if not exists with id, email, name, country attribute

CREATE TABLE IF NOT EXISTS users (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, email VARCHAR(255) NOT NULL UNIQUE, name VARCHAR(255), country CHAR(2) CHECK (country IN('US', 'CO', 'IN')) NOT NULL DEFAULT 'US');

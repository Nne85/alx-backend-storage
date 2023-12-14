-- Initial
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS orders;

CREATE TABLE IF NOT EXISTS items (
	    name VARCHAR(255) NOT NULL,
	    quantity int NOT NULL DEFAULT 10
);

CREATE TABLE IF NOT EXISTS orders (
	item_name VARCHAR(255) NOT NULL,
	number int NOT NULL
);

INSERT INTO items (name) VALUES ("apple"), ("pineapple"), ("pear");
INSERT INTO items (name, quantity) VALUES ("cake", 5), ("bread", 8), ("butter", 6);
INSERT INTO orders (item_name, number) VALUES ("bread", 5), ("cake", 5);

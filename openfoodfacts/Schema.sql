#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sate names utf8mb4 ;
# Convertir en utf8mb4 :  ALTER DATABASE pur_beurre_travaille CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;

# Lire le script en mysql : source C:/Users/khale/Desktop/Workspace/P5/openfoodfacts/Schema.sql;
# "alter table DemoTable1811 ADD UNIQUE unique_index_first_last_name(FirstName, LastName);"
DELETE FROM product_brand;
DELETE FROM product_store;
DELETE FROM product_category;
DELETE FROM product;
DELETE FROM category;
DELETE FROM brand;
DELETE FROM store;


DROP TABLE product_brand;
DROP TABLE product_store;
DROP TABLE product_category;
DROP TABLE category;
DROP TABLE brand;
DROP TABLE store;
DROP TABLE product;

# ajouter des elements dans product

CREATE TABLE product (
	id INT NOT NULL AUTO_INCREMENT,
	url VARCHAR(600),
	name VARCHAR(400),
	nutriscore VARCHAR(1),
	novascore VARCHAR(1),
	substitut_id INT DEFAULT NULL,
	PRIMARY KEY(id),
	CONSTRAINT uc_name UNIQUE (name)	
);

CREATE TABLE category (
	id INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(400),
	PRIMARY KEY(id),
	CONSTRAINT uc_name UNIQUE (name)
)CHARACTER SET utf8;


CREATE TABLE brand (
	id INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(400),
	PRIMARY KEY(id),
	CONSTRAINT uc_name UNIQUE (name)
)CHARACTER SET utf8;

CREATE TABLE store (
	id INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(400),
	PRIMARY KEY(id),
	CONSTRAINT uc_name UNIQUE (name)
)CHARACTER SET utf8;

CREATE TABLE product_category (
	product_id INT NOT NULL,
	category_id INT NOT NULL
)CHARACTER SET utf8;

CREATE TABLE product_brand (
	product_id INT NOT NULL,
	brand_id INT NOT NULL
)CHARACTER SET utf8;

CREATE TABLE product_store (
	product_id INT NOT NULL,
	store_id INT NOT NULL
)CHARACTER SET utf8;

ALTER TABLE product ADD FOREIGN KEY (substitut_id) REFERENCES product(id);
ALTER TABLE product_category ADD FOREIGN KEY (product_id) REFERENCES product(id);
ALTER TABLE product_category ADD FOREIGN KEY (category_id) REFERENCES category(id);

ALTER TABLE product_brand ADD FOREIGN KEY (product_id) REFERENCES product(id);
ALTER TABLE product_brand ADD FOREIGN KEY (brand_id) REFERENCES brand(id);

ALTER TABLE product_store ADD FOREIGN KEY (product_id) REFERENCES product(id);
ALTER TABLE product_store ADD FOREIGN KEY (store_id) REFERENCES store(id);
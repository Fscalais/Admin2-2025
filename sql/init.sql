CREATE DATABASE IF NOT EXISTS woodytoys;
USE woodytoys;
CREATE TABLE IF NOT EXISTS products (
  id MEDIUMINT(8) UNSIGNED NOT NULL AUTO_INCREMENT,
  product_name VARCHAR(255) DEFAULT NULL,
  product_price VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (id)
);
INSERT INTO products (product_name,product_price) VALUES
 ("Set de 100 cubes multicolores","50"),
 ("Yoyo","10"),
 ("Circuit de billes","75"),
 ("Arc à flèches","20"),
 ("Maison de poupées","150")
ON DUPLICATE KEY UPDATE product_name=VALUES(product_name), product_price=VALUES(product_price);



CREATE USER IF NOT EXISTS 'wt-user'@'php' IDENTIFIED BY 'wt-pwd';
GRANT SELECT ON `woodytoys`.* TO 'wt-user'@'php';
FLUSH PRIVILEGES;

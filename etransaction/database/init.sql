create database IF NOT EXISTS transactions;

use transactions;

CREATE TABLE transactions (
 id INT PRIMARY KEY AUTO_INCREMENT,
  buyer_id INT NOT NULL,
  seller_id INT NOT NULL,
  intermediary_id INT NOT NULL,
  amount DECIMAL(10, 2) NOT NULL,
  timestamp DATETIME NOT NULL,
  signature VARCHAR(255) NOT NULL,
  FOREIGN KEY (buyer_id) REFERENCES users(id),
  FOREIGN KEY (seller_id) REFERENCES users(id),
  FOREIGN KEY (intermediary_id) REFERENCES users(id)
);
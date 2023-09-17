import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="huycuong",
  password="nt219n21antt",
  database="payments"
)

mycursor = mydb.cursor()

#mycursor.execute("DROP DATABASE payments")
#mycursor.execute("CREATE DATABASE payments")


# #CREATE TABLE:
# mycursor.execute("CREATE TABLE users (id INT(11) NOT NULL AUTO_INCREMENT, username VARCHAR(50) NOT NULL, password VARCHAR(255) NOT NULL, email VARCHAR(100) NOT NULL, balance FLOAT NOT NULL DEFAULT 0,role VARCHAR(20) NOT NULL, created_at DATETIME DEFAULT CURRENT_TIMESTAMP, updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, PRIMARY KEY (id))")
# mycursor.execute("CREATE TABLE orders (id INT(11) NOT NULL AUTO_INCREMENT, user_id INT(11) NOT NULL, status VARCHAR(20) NOT NULL, created_at DATETIME DEFAULT CURRENT_TIMESTAMP, updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, PRIMARY KEY (id), FOREIGN KEY (user_id) REFERENCES users(id) )")
# mycursor.execute("CREATE TABLE transactions (id INT(11) NOT NULL AUTO_INCREMENT, client_id INT(11) NOT NULL, merchant_id INT(11) NOT NULL, order_id INT(11) NOT NULL, amount FLOAT NOT NULL, description TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP, updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, PRIMARY KEY (id), FOREIGN KEY (client_id) REFERENCES users(id), FOREIGN KEY (merchant_id) REFERENCES users(id), FOREIGN KEY (order_id) REFERENCES orders(id))")
# mycursor.execute("CREATE TABLE products ( id INT(11) NOT NULL AUTO_INCREMENT, name VARCHAR(50) NOT NULL, description TEXT, price FLOAT NOT NULL, created_at DATETIME DEFAULT CURRENT_TIMESTAMP, updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, PRIMARY KEY (id) )")
# mycursor.execute("CREATE TABLE order_items ( id INT(11) NOT NULL AUTO_INCREMENT, order_id INT(11) NOT NULL, product_id INT(11) NOT NULL, quantity INT(11) NOT NULL, price FLOAT NOT NULL, created_at DATETIME DEFAULT CURRENT_TIMESTAMP, updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, PRIMARY KEY (id), FOREIGN KEY (order_id) REFERENCES orders(id), FOREIGN KEY (product_id) REFERENCES products(id) )")
# mycursor.execute("CREATE TABLE shipping_addresses ( id INT(11) NOT NULL AUTO_INCREMENT, user_id INT(11) NOT NULL, name VARCHAR(50) NOT NULL, address TEXT NOT NULL, city VARCHAR(50) NOT NULL, state VARCHAR(50) NOT NULL, zip_code VARCHAR(10) NOT NULL, created_at DATETIME DEFAULT CURRENT_TIMESTAMP, updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, PRIMARY KEY (id), FOREIGN KEY (user_id) REFERENCES users(id) )")
# mycursor.execute("CREATE TABLE billing_addresses ( id INT(11) NOT NULL AUTO_INCREMENT, user_id INT(11) NOT NULL, name VARCHAR(50) NOT NULL, address TEXT NOT NULL, city VARCHAR(50) NOT NULL, state VARCHAR(50) NOT NULL, zip_code VARCHAR(10) NOT NULL, created_at DATETIME DEFAULT CURRENT_TIMESTAMP, updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, PRIMARY KEY (id), FOREIGN KEY (user_id) REFERENCES users(id) )")

#INSERT TABLE:
#User
# sql = "INSERT INTO users (username, password, email, balance, role) VALUES (%s, %s, %s, %s, %s)"
# val = [
#   ('GiaKhanh', '123456789', 'GiaKhanh@gmail.com', 100.0, "client"),
#   ('NgocThien', '123456789', 'NgocThien@gmail.com', 200.0, "client"),
#   ('HuyCuong', '123456789', 'HuyCuong@gmail.com', 300.0, "client"),
#   ('Bill Gates', '123456789', 'Gates@gmail.com', 400.0, "merchant"),
#   ('Elon Musk', '123456789', 'Musk@gmail.com', 500.0, "merchant")
# ]
# mycursor.executemany(sql, val)

# mydb.commit()
# print(mycursor.rowcount, "record inserted.")

#Orders
# sql = "INSERT INTO orders (user_id, status) VALUES (%s, %s)"
# val = [
#   (1, 'pending'),
#   (2, 'processing'),
#   (3, 'completed'),
#   (4, 'cancelled'),
#   (5, 'pending')
# ]
# mycursor.executemany(sql, val)

# mydb.commit()
# print(mycursor.rowcount, "record inserted.")


#Transacstions
# sql = "INSERT INTO transactions (client_id, merchant_id, order_id, amount, description) VALUES (%s, %s, %s, %s, %s)"
# val = [
#   (1, 2, 1, 50.0, 'Payment for order 1'),
#   (2, 3, 2, 75.0, 'Payment for order 2'),
#   (3, 4, 3, 100.0, 'Payment for order 3'),
#   (4, 5, 4, 125.0, 'Payment for order 4'),
#   (5, 1, 5, 150.0, 'Payment for order 5')
# ]
# mycursor.executemany(sql, val)

# mydb.commit()
# print(mycursor.rowcount, "record inserted.")

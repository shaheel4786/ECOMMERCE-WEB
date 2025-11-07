# 🛍️ E-Commerce Web Application (with Razorpay Wallet Integration)

A simple and fully functional **E-Commerce Web App** built using **Flask, MySQL, and Razorpay**.
Users can browse products, add to cart, make payments through Razorpay, and maintain a wallet balance.

---

## 🚀 Features

- 🧾 User-friendly Product Listing
- 🛒 Add to Cart & Checkout
- 💰 Razorpay Payment Gateway Integration
- 👛 Wallet Balance System (Add Money, Update on Payment)
- 🔍 Product Search
- 📱 Responsive UI using HTML + Bootstrap

---

## ⚙️ Tech Stack

| Component | Technology Used |
|------------|----------------|
| Frontend | HTML, CSS, Bootstrap |
| Backend | Python (Flask Framework) |
| Database | MySQL |
| Payment Gateway | Razorpay API |
| Version Control | Git, GitHub |

---

## 🧩 Installation Steps

1. Clone this repository  
   ```bash
   git clone https://github.com/your-username/ecommerce-project.git
   cd ecommerce-project

2. Install dependencies

pip install flask flask-mysqldb razorpay


3. Configure Database

Create a MySQL database named ecommerce_db

Import your SQL file or manually create tables (users, products, cart)

4. Set Razorpay Keys
Inside app.py, replace:

RAZORPAY_KEY_ID = "rzp_test_XXXX"
RAZORPAY_KEY_SECRET = "XXXX"


5. Run the server

python app.py


Then open: http://127.0.0.1:5000

💳 Razorpay Test Card Details
Field	Value
Card Number	4111 1111 1111 1111

Expiry	12/29

CVV	123

OTP	123456


## 📸 Screenshots

Page	Screenshot
Home Page	

Product Detail	

Cart	

Add Balance	

Razorpay Checkout	

Payment Success	

## SQL structure

🧩 Step 1: Create the database
CREATE DATABASE ecommerce_db;
USE ecommerce_db;

🧾 Step 2: Create the users table

This table stores each user’s login info and wallet balance.

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    balance DECIMAL(10,2) DEFAULT 0.00
);


👉 You can manually add a user for testing:

INSERT INTO users (name, email, password, balance)
VALUES ('Shaheel', 'shaheel@example.com', '1234', 0.00);

🧺 Step 3: Create the products table

Stores all available products in the store.

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    price DECIMAL(10,2),
    image VARCHAR(255),
    details TEXT,
    faq TEXT
);


Example test data:

INSERT INTO products (name, description, price, image, details, faq)
VALUES
('Bluetooth Headphones', 'Wireless over-ear headphones with mic', 1999.00, 'headphone.jpg', '10hr Battery Backup', '1 Year Warranty'),
('Smart Watch', 'Fitness tracker with heart rate sensor', 1499.00, 'watch.jpg', 'Touch Screen, Waterproof', '6 Months Warranty');

🛒 Step 4: Create the cart table

Stores the items added to a user’s cart.

CREATE TABLE cart (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    quantity INT DEFAULT 1,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

🪙 Step 5: (Optional) Create the transactions table

If you want to record successful Razorpay payments later:

CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    order_id VARCHAR(100),
    amount DECIMAL(10,2),
    payment_id VARCHAR(100),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

✅ Step 6: Check all tables

After typing everything, confirm with:

SHOW TABLES;


You should see:

+----------------+
| Tables_in_ecommerce_db |
+----------------+
| cart           |
| products       |
| transactions   |
| users          |
+----------------+





## 👨‍💻 Developed By

Shaheel K P
MCA 2025 – MES College of Engineering, Kuttippuram

📧 sshaheelkp@gmail.com

📞 9496972694

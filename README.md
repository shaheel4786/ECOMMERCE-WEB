🛍️ E-Commerce Web Application (with Razorpay Wallet Integration)

A simple and fully functional E-Commerce Web App built using Flask, MySQL, and Razorpay.
Users can browse products, add to cart, make payments through Razorpay, and maintain a wallet balance.

🚀 Features

🧾 User-friendly Product Listing

🛒 Add to Cart & Checkout

💰 Razorpay Payment Gateway Integration

👛 Wallet Balance System (Add Money, Update on Payment)

🔍 Product Search

📱 Responsive UI using HTML + Bootstrap

⚙️ Tech Stack
Component	Technology Used
Frontend	HTML, CSS, Bootstrap
Backend	Python (Flask Framework)
Database	MySQL
Payment Gateway	Razorpay API
Version Control	Git, GitHub
🧩 Installation Steps

Clone this repository

git clone https://github.com/your-username/ecommerce-project.git
cd ecommerce-project


Install dependencies

pip install flask flask-mysqldb razorpay


Configure Database

Create a MySQL database named ecommerce_db

Import your SQL file or manually create tables (users, products, cart)

Set Razorpay Keys
Inside app.py, replace:

RAZORPAY_KEY_ID = "rzp_test_XXXX"
RAZORPAY_KEY_SECRET = "XXXX"


Run the server

python app.py


Then open http://127.0.0.1:5000

💳 Razorpay Test Card Details

Use the following test card during development:

Field	Value
Card Number	4111 1111 1111 1111
Expiry	Any future date (e.g., 12/29)
CVV	123
OTP	123456
📸 Screenshots
Page	Screenshot
Home Page	

Product Detail	

Cart	

Add Balance	

Razorpay Checkout	

Payment Success	

👨‍💻 Developed By

Shaheel K P
MCA, 2025 – MES College of Engineering, Kuttippuram
📧 sshaheelkp@gmail.com

📞 9496972694

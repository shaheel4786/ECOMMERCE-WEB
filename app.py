from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import razorpay
from flask import request, jsonify
from flask import Flask, render_template, request, redirect, url_for, session, flash


# Replace these with your actual Razorpay keys
RAZORPAY_KEY_ID = "YOUR RAZORPAY_KEY_ID"
RAZORPAY_KEY_SECRET = "RAZORPAY_KEY_ID RAZORPAY_KEY_SECRET"

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))


app = Flask(__name__)
app.secret_key = 'shaheel123'
@app.route('/create_order', methods=['POST'])
def create_order():
    amount = int(float(request.form['amount']) * 100)  # Convert safely to paise
    currency = "INR"

    data = {
        "amount": amount,
        "currency": currency,
        "payment_capture": 1
    }

    order = razorpay_client.order.create(data=data)
    return jsonify({
        "key": RAZORPAY_KEY_ID,
        "amount": amount,
        "currency": currency,
        "order_id": order['id']
    })

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456789'
app.config['MYSQL_DB'] = 'ecommerce_db'

mysql = MySQL(app)
@app.route('/payment_success', methods=['POST'])

# Home page - list all products
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()
    return render_template('index.html', products=products)
@app.route('/add_balance', methods=['GET', 'POST'])
def add_balance():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        user_id = session.get('user_id')
        order = razorpay_client.order.create({
            'amount': int(amount * 100),  # in paise
            'currency': 'INR',
            'payment_capture': 1
        })
        return render_template('payment.html', order=order, amount=amount)
    return render_template('add_balance.html') 

# Search products
@app.route('/search')
def search():
    query = request.args.get('query', '').strip()
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * FROM products WHERE name LIKE %s OR description LIKE %s",
        (f"%{query}%", f"%{query}%")
    )
    products = cur.fetchall()
    cur.close()
    if products:
        flash(f"Showing results for '{query}'")
    else:
        flash(f"No products found for '{query}'")
    return render_template('index.html', products=products)


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    cur = mysql.connection.cursor()
    # Select only the desired columns
    cur.execute("""
        SELECT id, name, description, price, image, details, faq 
        FROM products 
        WHERE id=%s
    """, (product_id,))
    product = cur.fetchone()
    cur.close()
    return render_template('product_detail.html', product=product)

# Buy Now page
@app.route('/buy_now/<int:product_id>', methods=['GET', 'POST'])
@app.route('/buy_now/<int:product_id>')
def buy_now(product_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cur.fetchone()
    cur.close()

    # Send product info to Razorpay JS
    return render_template('buy_now.html', product=product, razorpay_key=RAZORPAY_KEY_ID)

@app.route('/update_quantity/<int:product_id>', methods=['POST'])
def update_quantity(product_id):
    new_quantity = int(request.form['quantity'])
    cur = mysql.connection.cursor()
    cur.execute("UPDATE cart SET quantity = %s WHERE product_id = %s", (new_quantity, product_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('cart'))

@app.route('/buy_cart', methods=['POST'])
def buy_cart():
    cur = mysql.connection.cursor()
    # get all cart items
    cur.execute("""
        SELECT products.id, products.name, SUM(cart.quantity) 
        FROM cart
        JOIN products ON cart.product_id = products.id
        GROUP BY products.id, products.name
    """)
    cart_items = cur.fetchall()
    cur.close()

    # Here you can process the order (e.g., save to orders table)
    flash("✅ Order placed successfully for all cart items!")
    
    # Clear the cart
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM cart")
    mysql.connection.commit()
    cur.close()

    return redirect('/')
 
@app.route('/cart')
def cart():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT 
            products.id,
            products.name,
            products.price,
            products.image,
            SUM(cart.quantity) AS total_quantity
        FROM cart
        JOIN products ON cart.product_id = products.id
        GROUP BY products.id, products.name, products.price, products.image
    """)
    cart_items = cur.fetchall()
    total_amount = sum(item[2] * item[4] for item in cart_items)
    cur.close()
    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)




@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO cart (product_id, quantity) VALUES (%s, 1)", (product_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('cart'))

# Clear cart
@app.route('/clear_cart')
def clear_cart():
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM cart")
    mysql.connection.commit()
    cur.close()
    flash("Cart cleared ✅")
    return redirect('/')

@app.route('/checkout_cart')
def checkout_cart():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT 
            products.id,
            products.name,
            products.price,
            products.image,
            SUM(cart.quantity) AS total_quantity
        FROM cart
        JOIN products ON cart.product_id = products.id
        GROUP BY products.id, products.name, products.price, products.image
    """)
    rows = cur.fetchall()
    cur.close()

    # Convert tuples to dictionaries (just like in /cart)
    cart_items = [
        {
            'id': row[0],
            'name': row[1],
            'price': row[2],
            'image': row[3],
            'total_quantity': row[4]
        }
        for row in rows
    ]

    total_amount = sum(item['price'] * item['total_quantity'] for item in cart_items)

    return render_template('checkout_cart.html', cart_items=cart_items, total_amount=total_amount)

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM cart WHERE product_id = %s", (product_id,))
    mysql.connection.commit()
    cur.close()
    flash("Item removed successfully!", "success")
    return redirect(url_for('cart'))


@app.route('/balance')
def balance():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')

    cur = mysql.connection.cursor()
    cur.execute("SELECT balance FROM users WHERE id = %s", (user_id,))
    result = cur.fetchone()
    cur.close()

    if result:
        balance = result[0]
    else:
        balance = 0.0

    return render_template("balance.html", balance=balance)
@app.route('/payment_success', methods=['POST'])
def payment_success():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No payment data received"}), 400

    payment_id = data.get('razorpay_payment_id')
    order_id = data.get('razorpay_order_id')
    signature = data.get('razorpay_signature')

    # Optional: verify signature for security (you can add later)

    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Login required"}), 403

    # Convert amount from paise to rupees
    amount = float(data.get('amount', 0)) / 100

    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET balance = balance + %s WHERE id = %s", (amount, user_id))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Payment successful! Wallet updated."})

 
if __name__ == '__main__':
    app.run(debug=True)

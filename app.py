from flask import Flask, render_template, redirect, request, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'shaheel123'

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456789'
app.config['MYSQL_DB'] = 'ecommerce_db'

mysql = MySQL(app)

# Home page - list all products
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()
    return render_template('index.html', products=products)

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

# Product detail page
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cur.fetchone()
    cur.close()
    return render_template('product_detail.html', product=product)

# Buy Now page
@app.route('/buy_now/<int:product_id>', methods=['GET', 'POST'])
def buy_now(product_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        # Optional: save order to database
        flash(f"✅ Order placed successfully! Thank you {name} for purchasing {product[1]}.")
        return redirect('/')

    return render_template('checkout.html', product=product)

# Cart page
@app.route('/cart')
def cart():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT cart.id, products.name, products.price, cart.quantity
        FROM cart
        JOIN products ON cart.product_id = products.id
    """)
    cart_items = cur.fetchall()
    cur.close()
    return render_template('cart.html', cart_items=cart_items)

# Add to cart
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO cart(product_id, quantity) VALUES(%s, %s)", (product_id, 1))
    mysql.connection.commit()
    cur.close()
    flash("Product added to cart ✅")
    return redirect('/cart')

# Clear cart
@app.route('/clear_cart')
def clear_cart():
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM cart")
    mysql.connection.commit()
    cur.close()
    flash("Cart cleared ✅")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

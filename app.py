from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret123'

# ---------------- DATABASE SETUP ----------------
def init_db():
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()

    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT,
                    password TEXT,
                    address TEXT,
                    mobile TEXT
                )''')

    # Create products table
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    price INTEGER
                )''')

    conn.commit()
    conn.close()

# ---------------- ROUTES ----------------
@app.route('/')
def home():
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.close()
    return render_template('home.html', products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
        mobile = request.form['mobile']

        conn = sqlite3.connect('ecommerce.db')
        c = conn.cursor()
        c.execute(
            "INSERT INTO users (name,email,password,address,mobile) VALUES (?,?,?,?,?)",
            (name, email, password, address, mobile)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('ecommerce.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['user'] = user[1]
            return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

# ---------------- MAIN ----------------
if __name__ == '__main__':
    init_db()

    # Insert sample products (only once)
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()

    # Check if products already exist
    c.execute("SELECT COUNT(*) FROM products")
    count = c.fetchone()[0]

    if count == 0:
        c.execute("INSERT INTO products (name, price) VALUES ('T-Shirt', 500)")
        c.execute("INSERT INTO products (name, price) VALUES ('Shoes', 1200)")

    conn.commit()
    conn.close()

    app.run(host='0.0.0.0', port=5000, debug=True)

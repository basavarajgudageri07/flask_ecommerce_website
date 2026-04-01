from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# -------- DB INIT --------
def init_db():
    conn = sqlite3.connect("ecommerce.db")
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, email TEXT, password TEXT,
        address TEXT, mobile TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, price INTEGER, category TEXT, image TEXT)''')

    conn.commit()
    conn.close()

init_db()

# -------- INSERT PRODUCTS --------
def insert_products():
    conn = sqlite3.connect("ecommerce.db")
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM products")
    if c.fetchone()[0] == 0:
        products = [
            ("Running Shoes",2000,"Shoes","shoes.jpg"),
            ("Summer Dress",1500,"Dress","dress.jpg"),
            ("Smartphone",30000,"Mobiles","mobile.jpg"),
            ("Laptop",55000,"Laptops","laptop.jpg"),
            ("Perfume",1200,"Perfumes","perfume.jpg"),
            ("Books",800,"Books","books.jpg"),
            ("Pen",200,"Stationery","pen.jpg"),
            ("Watch",2500,"Accessories","watch.jpg"),
            ("Charger",500,"Electronics","charger.jpg"),
            ("Headphones",1500,"Electronics","headphones.jpg"),
            ("Soccer Ball",700,"Sports","soccer.jpg"),
            ("Board",1200,"Furniture","board.jpg")
        ]
        c.executemany("INSERT INTO products(name,price,category,image) VALUES (?,?,?,?)", products)
        conn.commit()

    conn.close()

insert_products()

# -------- HOME --------
@app.route('/')
def home():
    conn = sqlite3.connect("ecommerce.db")
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.close()

    user = session.get('user')
    return render_template("home.html", products=products, user=user)

# -------- REGISTER --------
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        data = (
            request.form['name'],
            request.form['email'],
            request.form['password'],
            request.form['address'],
            request.form['mobile']
        )

        conn = sqlite3.connect("ecommerce.db")
        c = conn.cursor()
        c.execute("INSERT INTO users(name,email,password,address,mobile) VALUES (?,?,?,?,?)", data)
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template("register.html")

# -------- LOGIN --------
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        conn = sqlite3.connect("ecommerce.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=? AND password=?",
                  (request.form['email'], request.form['password']))
        user = c.fetchone()
        conn.close()

        if user:
            session['user'] = user[1]
            return redirect('/')

    return render_template("login.html")

# -------- CART --------
@app.route('/add/<int:id>')
def add(id):
    cart = session.get('cart', {})
    cart[str(id)] = cart.get(str(id), 0) + 1
    session['cart'] = cart
    return redirect('/')

@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    conn = sqlite3.connect("ecommerce.db")
    c = conn.cursor()

    items = []
    for pid, qty in cart.items():
        c.execute("SELECT * FROM products WHERE id=?", (pid,))
        items.append((c.fetchone(), qty))

    conn.close()
    return render_template("cart.html", items=items)

# -------- LOGOUT --------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# -------- RUN --------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

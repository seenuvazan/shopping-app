import json
from flask import Flask, render_template, redirect, url_for, request, flash, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Files for storing data
USERS_FILE = "users.json"
PRODUCTS_FILE = "products.json"

# Helper functions
def load_users():
    try:
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file)

def load_products():
    try:
        with open(PRODUCTS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_products(products):
    with open(PRODUCTS_FILE, "w") as file:
        json.dump(products, file)

@app.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    return redirect(url_for("home"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        users = load_users()
        user = next((user for user in users if user['username'] == username), None)
        if user and user['password'] == password:
            session['user'] = username
            return redirect(url_for("home"))
        flash("Invalid username or password", "danger")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        users = load_users()
        if any(user['username'] == username for user in users):
            flash("Username already exists!", "danger")
            return redirect(url_for("register"))
        users.append({"username": username, "password": password})
        save_users(users)
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for("login"))

@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("home.html")

@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        description = request.form["description"]
        products = load_products()
        products.append({"name": name, "price": price, "description": description})
        save_products(products)
        flash("Product added successfully!", "success")
        return redirect(url_for("home"))
    return render_template("add_product.html")

@app.route("/view_products")
def view_products():
    if "user" not in session:
        return redirect(url_for("login"))
    products = load_products()
    return render_template("view_products.html", products=products)

if __name__ == "__main__":
    app.run(debug=True)

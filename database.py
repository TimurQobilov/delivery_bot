import sqlite3
from datetime import datetime

from telebot.util import user_link

connection = sqlite3.connect("fake_kfc.db")
sql = connection.cursor()

sql.execute("CREATE TABLE IF NOT EXISTS users "
            "(user_id INTEGER, name TEXT, "
            "phone_number TEXT, reg_date DATETIME);")
sql.execute("CREATE TABLE IF NOT EXISTS products "
            "(pr_id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "pr_name TEXT, pr_quantity INTEGER, pr_price REAL,"
            "pr_desc TEXT, pr_photo TEXT, reg_date DATETIME);")
sql.execute("CREATE TABLE IF NOT EXISTS cart (user_id INTEGER,"
            "pr_id INTEGER, pr_count INTEGER, pr_name TEXT, "
            "total_price REAL);")
connection.commit()

def add_user(name, phone_number, user_id):
    connection = sqlite3.connect("fake_kfc.db")
    sql = connection.cursor()
    sql.execute(f"INSERT INTO users (user_id, name, phone_number, reg_date) "
                "VALUES (?, ?, ?, ?);", (user_id, name, phone_number, datetime.now()))
    connection.commit()

def check_user(user_id):
    connection = sqlite3.connect("fake_kfc.db")
    sql = connection.cursor()
    checker = sql.execute("SELECT * FROM users WHERE user_id=?", (user_id, )).fetchone()
    if checker:
        return True
    elif not checker:
        return False
def get_all_users():
    connection = sqlite3.connect("fake_kfc.db")
    sql = connection.cursor()
    all_users = sql.execute("SELECT * FROM users;").fetchall()
    return all_users
# продукты
def add_product(pr_name, pr_price, pr_desc, pr_quantity, pr_photo):
    connection = sqlite3.connect("fake_kfc.db")
    sql = connection.cursor()
    sql.execute("INSERT INTO products (pr_name, pr_price, pr_desc, pr_quantity, "
                "pr_photo, reg_date) VALUES (?, ?, ?, ?, ?, ?);",
                (pr_name, pr_price, pr_desc, pr_quantity, pr_photo, datetime.now()))
    connection.commit()
def get_all_products():
    connection = sqlite3.connect("fake_kfc.db")
    sql = connection.cursor()
    all_products = sql.execute("SELECT * FROM products;").fetchall()
    return all_products
def delete_product(pr_id):
    connection = sqlite3.connect("fake_kfc.db")
    sql = connection.cursor()
    sql.execute("DELETE FROM products WHERE pr_id=?;", (pr_id,))
    connection.commit()

def get_exact_product(pr_id):
    connection = sqlite3.connect("fake_kfc.db")
    sql = connection.cursor()
    exact_product = sql.execute("SELECT pr_name, pr_price, pr_desc, pr_photo "
                                "FROM products WHERE pr_id=?;", (pr_id,)).fetchone()
    return  exact_product

def get_pr_id_name():
    connection = sqlite3.connect("fake_kfc.db")
    sql = connection.cursor()
    all_products = sql.execute("SELECT pr_id, pr_name, pr_quantity"
                               "FROM products;").fetchall()

    actual_products = [[product[0],product[1]] for product in all_products if product[2] > 0]

def delete_all_products():
    connection = sqlite3.connect("fake_kfc.db")
    sql = connection.cursor()
    sql.execute("DELETE FROM products;")
    connection.commit()

def change_quantity(pr_id, pr_quantity):
    connection = sqlite3.connect("fake_kfc.db")
    sql = connection.cursor()
    sql.execute("UPDATE products SET pr_quantity=? WHERE pr_id=?;", (pr_quantity,pr_id))
    connection.commit()

def add_to_cart(user_id, pr_id, pr_name, pr_count, pr_price):
    connection = sqlite3.connect("fake_kfc.db")
    sql = connection.cursor()
    total_price = pr_price * pr_count
    sql.execute("INSERT INTO cart (user_ud, pr_id, pr_name,"
                "pr_count, total_price) VALUES (?,?,?,?,?);",
                (user_id, pr_id, pr_name, pr_count, total_price))
    connection.commit()

def get_cart_id_name(user_id):
    connection = sqlite3.connect("fake_kfc.db")
    sql = connection.cursor()
    product = sql.execute("SELECT pr_id, pr_name FROM cart WHERE user_id=?;",
                          (user_id,)).fetchall()
    return product


def delete_exact_product(user_id, pr_id):
    connection = sqlite3.connect("fake_kfc.db")
    sql = connection.cursor()
    sql.execute("DELETE FROM cart WHERE user_id=? and pr_id=?;",
                (user_id, pr_id))
    connection.commit()


def delete_user_cart(user_id):
    connection = sqlite3.connect("fake_kfc.db")
    sql = connection.cursor()
    sql.execute("DELETE FROM cart WHERE user_id=?;", (user_id,))
    connection.commit()


def get_user_cart(user_id):
    connection = sqlite3.connect("fake_kfc.db")
    sql = connection.cursor()
    cart_items = sql.execute("SELECT pr_name, pr_count, total_price FROM cart WHERE user_id=?;", (user_id,)).fetchall()
    return cart_items  # Формат: [(Название, Количество, Цена), ...]








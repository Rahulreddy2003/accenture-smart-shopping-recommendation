import sqlite3

def get_db_connection():
    conn = sqlite3.connect("smart_shopping.db")
    conn.row_factory = sqlite3.Row
    return conn

def fetch_all_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    conn.close()
    return [dict(product) for product in products]

def get_products_by_categories(categories: list):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM Products WHERE category IN ({seq})".format(
        seq=", ".join(["?"] * len(categories))
    )
    cursor.execute(query, categories)
    products = cursor.fetchall()
    conn.close()
    return [dict(product) for product in products]

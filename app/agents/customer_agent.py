import sqlite3

def get_db_connection():
    conn = sqlite3.connect("smart_shopping.db")
    conn.row_factory = sqlite3.Row
    return conn

def fetch_all_customers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    conn.close()
    return [dict(user) for user in users]

def get_customer_preferences(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT preferences FROM Users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user["preferences"].split(", ") if user else None

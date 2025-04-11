import sqlite3

def recommend_products_for_user(user_id: int):
    conn = sqlite3.connect("smart_shopping.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT preferences FROM Users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        return []

    preferences = user["preferences"].split(", ")

    query = "SELECT * FROM Products WHERE category IN ({})".format(
        ",".join(["?"] * len(preferences))
    )
    cursor.execute(query, preferences)
    products = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in products]

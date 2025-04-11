import sqlite3

conn = sqlite3.connect("smart_shopping.db")
cursor = conn.cursor()

# Drop existing tables if any (optional but useful for resetting)
cursor.execute("DROP TABLE IF EXISTS Users")
cursor.execute("DROP TABLE IF EXISTS Products")

# Create Users table
cursor.execute('''
    CREATE TABLE Users (
        user_id INTEGER PRIMARY KEY,
        name TEXT,
        preferences TEXT
    )
''')

# Create Products table
cursor.execute('''
    CREATE TABLE Products (
        product_id INTEGER PRIMARY KEY,
        name TEXT,
        category TEXT,
        price REAL
    )
''')

# Insert sample users
users = [
    (1, "Rahul", "Electronics, Fashion"),
    (2, "Sneha", "Books, Beauty"),
    (3, "Arjun", "Groceries, Electronics")
]
cursor.executemany("INSERT INTO Users VALUES (?, ?, ?)", users)

# Insert sample products
products = [
    (1, "Smartphone", "Electronics", 999.99),
    (2, "T-shirt", "Fashion", 19.99),
    (3, "Shampoo", "Beauty", 5.49),
    (4, "Novel", "Books", 12.99),
    (5, "Rice Bag", "Groceries", 25.00),
    (6, "Headphones", "Electronics", 49.99),
]
cursor.executemany("INSERT INTO Products VALUES (?, ?, ?, ?)", products)

conn.commit()
conn.close()

print("Database populated with sample data! ✅")

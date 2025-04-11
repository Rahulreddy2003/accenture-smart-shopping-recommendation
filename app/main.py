from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.agents.customer_agent import fetch_all_customers
from app.agents.product_agent import fetch_all_products


import sqlite3

app = FastAPI()

# DB Connection
def get_db_connection():
    conn = sqlite3.connect("smart_shopping.db")
    conn.row_factory = sqlite3.Row
    return conn

# ------------------ Models ------------------
class QueryRequest(BaseModel):
    user_id: int
    query: str

# ------------------ Home Routes ------------------
@app.get("/")
def home():
    return {"status": "success", "message": "Welcome to Smart Shopping API!"}

# ------------------ Dummy Query API ------------------
database = []

@app.post("/submit/")
def submit_query(request: QueryRequest):
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    database.append(request.dict())
    return {"message": "Query submitted successfully!", "data": request}

@app.get("/queries/")
def get_queries():
    return {"total_queries": len(database), "queries": database}

# ------------------ Smart Shopping APIs ------------------

@app.get("/recommendations/{user_id}")
def get_recommendations(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch user preferences
    cursor.execute("SELECT preferences FROM Users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    preferences = user["preferences"].split(", ")

    # Fetch products matching user preferences
    query = "SELECT * FROM Products WHERE category IN ({seq})".format(
        seq=", ".join(["?"] * len(preferences))
    )
    cursor.execute(query, preferences)
    products = cursor.fetchall()
    
    conn.close()
    return {"recommended_products": [dict(product) for product in products]}

@app.get("/users")
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    conn.close()
    return {"users": [dict(user) for user in users]}

@app.get("/products")
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    conn.close()
    return {"products": [dict(product) for product in products]}

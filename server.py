from flask import Flask, jsonify, request
import sqlite3

app= Flask(__name__) # Create an instance 

# *** UPPERCASES identifies a CONSTANT
DB_NAME = "online-store.db"

# UPPERCASES IS ALSO FOR SQL SINTAX
# lowercases is for bussines language (you can choose what name)
def init_db():
        connection = sqlite3.connect(DB_NAME) # opens a connection to the database file named online-store.db
        cursor = connection.cursor() # Creates a cursor/tool that lets you send commands (EXECUTE, SELECT, INSERT, ...) to the DB
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                price REAL NOT NULL,
                category TEXT NOT NULL,
                image TEXT NOT NULL
        )
        """)
        connection.commit() # Save changes to the DB
        connection.close() # Close the connection to the DB
    
@app.get("/api/health")
def health_check():
    return jsonify({
        "status" : "Ok"
    }),200


# POST /api/products -> Create a new product record to the DB.
@app.post("/api/products")
def create_product():
        new_product = request.get_json()
        name = new_product["name"]
        price = new_product["price"]
        category = new_product["category"]
        image = new_product["image"]
        
        connection = sqlite3.connect(DB_NAME) # Open the connection to the DB
        cursor = connection.cursor() # Creates a cursor/tool that lets you send commands
        cursor.execute("""
        INSERT INTO products (name, price, category, image)
        VALUES (?, ?, ?, ?)""", (name, price, category, image))
        connection.commit() # Save the changes to the DB
        connection.close() # Close the connection to the DB
        
        return jsonify({
            "message": "Product created successfully"
        }), 201 # Created

init_db()
app.run(debug=True) # Execute the instance
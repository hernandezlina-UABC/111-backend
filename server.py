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
        
        # COUPONS TABLE
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS coupons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL,
                discount INTEGER NOT NULL
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
        

# --------- COUPONS ----------
# Insert the 5 steps for the cretion of an endpoint
# POST /api/coupons -> creates a new coupon to the db
@app.post("/api/coupons")
def create_coupon():
    # Insert 5 SQL steps for the creating of a new record in coupons table
    new_coupon = request.get_json()
    code = new_coupon["code"]
    discount = new_coupon["discount"]
    
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
            INSERT INTO coupons (code, discount)
            VALUES (?, ?)""", (code, discount)
            )
    connection.commit()
    connection.close()
            
    return jsonify({
        "message": "Coupon created successfully"
    }), 201 
            

init_db()
app.run(debug=True) # Execute the instance
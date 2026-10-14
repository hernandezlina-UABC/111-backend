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
        

# GET /api/products -> returns all the products
@app.get("/api/products")
def get_products():
        connection = sqlite3.connect(DB_NAME)
        #.row make each row behave like a dictionary
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        # SELECT column_name1, column_name2 FROM products           
        cursor.execute("SELECT * FROM products")
        # fetchall retrieves all rows from the result of the query
        # fetchone retrieves one 
        products_db = cursor.fetchall()
        connection.close()
        
        print(products_db)
        products = []
        
        for product in products_db:
            products.append(dict(product))
        
        return jsonify({
            "success": True,
            "message": "Products retrieved successfully",
            "data": products
        }), 200
        

# GET /api/products/2 -> returns a product by id (path parameters)
@app.get("/api/products/<int:product_id>")
def get_product_by_id(product_id):
    
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product_db = cursor.fetchone()
    
    if not product_db:
        connection.close()
        return jsonify({
            "success":False,
            "message": "Product not found"       
    }), 404
        
    connection.close()
    product = dict(product_db)
    
    print(product_db)
    return jsonify({"success":True,
                    "message": "Product retrieved successfully",
                    "data": product,
    }), 200


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
    
    
#  GET /api/coupons -> returns all the coupons
@app.get("/api/coupons")
def get_coupons():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM coupons")
    coupons_db = cursor.fetchall()
    connection.close()
    
    print(coupons_db)    
    coupons = []
    
    for coupon in coupons_db:
        coupons.append(dict(coupon))
        
    return jsonify({
        "success": True,
        "message": "Coupons retrieved successfully",
        "data": coupons
    }), 200
          

# GET /api/coupons/2 -> returns a coupon by id (path parameters)
@app.get("/api/coupons/<int:coupon_id>")
def get_coupon_by_id(coupon_id):
        
        connection = sqlite3.connect(DB_NAME)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM coupons WHERE id = ?", (coupon_id,))
        coupon_db = cursor.fetchone()
        
        if not coupon_db:
                connection.close()
                return jsonify({
                    "success": False,
                    "message": "Coupon not found"       
        }),404
            
        connection.close()
        product = dict(coupon_db)
        
        print(coupon_db)
        return jsonify({"success":True,
                        "message": "Coupon retrieved successfully",
                        "data": product,
        }), 200
    
  

init_db()
app.run(debug=True) # Execute the instance
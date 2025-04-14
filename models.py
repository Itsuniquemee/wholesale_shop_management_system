import sqlite3

DB_NAME = "wholesale_shop.db"

# ✅ Database Connection
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")  # Enforce foreign key constraints
    return conn

# ✅ Add Supplier
def add_supplier(name, contact):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO suppliers (name, contact) VALUES (?, ?)", (name, contact))
    conn.commit()
    conn.close()

# ✅ Add Product
def add_product(name, supplier_id, stock, price):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, supplier_id, stock, price) VALUES (?, ?, ?, ?)", 
                   (name, supplier_id, stock, price))
    conn.commit()
    conn.close()

# ✅ Add Customer
def add_customer(name, contact):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customers (name, contact) VALUES (?, ?)", (name, contact))
    conn.commit()
    conn.close()

# ✅ Add Order
def add_order(customer_id, total_price):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (customer_id, total_price, date) VALUES (?, ?, datetime('now'))", 
                   (customer_id, total_price))
    conn.commit()
    conn.close()

# ✅ Get All Products
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return products

# ✅ Get All Suppliers
def get_suppliers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM suppliers")
    suppliers = cursor.fetchall()
    conn.close()
    return suppliers

# ✅ Get All Customers
def get_customers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    conn.close()
    return customers

# ✅ Sell Product
def sell_product(product_id, customer_id, quantity):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT stock, price FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()

    if product is None:
        conn.close()
        return "❌ Product not found."

    stock, price = product["stock"], product["price"]

    if stock < quantity:
        conn.close()
        return "❌ Not enough stock available."

    total_price = quantity * price

    cursor.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (quantity, product_id))
    cursor.execute("INSERT INTO sales (product_id, customer_id, quantity, total_price, sale_date) VALUES (?, ?, ?, ?, datetime('now'))",
                   (product_id, customer_id, quantity, total_price))

    conn.commit()
    conn.close()
    return f"✅ Sold {quantity} units of Product ID {product_id}."

# ✅ Get Sales History
def get_sales():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sales'")
    if not cursor.fetchone():
        conn.close()
        return []

    cursor.execute("""
        SELECT 
            s.id, 
            COALESCE(p.name, 'Deleted Product') AS product_name, 
            COALESCE(c.name, 'Deleted Customer') AS customer_name, 
            s.quantity, 
            s.total_price, 
            s.sale_date  
        FROM sales s
        LEFT JOIN products p ON s.product_id = p.id
        LEFT JOIN customers c ON s.customer_id = c.id
        ORDER BY s.sale_date DESC;
    """)

    sales = cursor.fetchall()
    conn.close()

    return [
        {
            "id": s["id"],
            "product": s["product_name"],
            "customer": s["customer_name"],
            "quantity": s["quantity"],
            "total_price": s["total_price"],
            "sale_date": s["sale_date"]
        }
        for s in sales
    ]

# ✅ Get All Orders
def get_orders():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders'")
    if not cursor.fetchone():
        conn.close()
        return []

    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    conn.close()
    return orders

# ✅ Get Dashboard Data
def get_dashboard_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT SUM(total_price) FROM orders")
    total_sales = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT SUM(stock) FROM products")
    total_products = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT COUNT(*) FROM customers")
    total_customers = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT COUNT(*) FROM suppliers")
    total_suppliers = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return total_sales, total_products, total_customers, total_suppliers

# ✅ Delete Product
def delete_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM sales WHERE product_id = ?", (product_id,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        return "❌ Cannot delete product. It has sales records."

    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    return "✅ Product deleted successfully."

# ✅ Delete Customer
def delete_customer(customer_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM sales WHERE customer_id = ?", (customer_id,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        return "❌ Cannot delete customer. They have purchase records."

    cursor.execute("SELECT COUNT(*) FROM orders WHERE customer_id = ?", (customer_id,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        return "❌ Cannot delete customer. They have order records."

    cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    conn.commit()
    conn.close()
    return "✅ Customer deleted successfully."

# ✅ Delete Order
def delete_order(order_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()
    return f"✅ Order ID {order_id} deleted successfully."

# ✅ Delete Supplier
def delete_supplier(supplier_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM products WHERE supplier_id = ?", (supplier_id,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        return "❌ Cannot delete supplier. They have associated products."

    cursor.execute("DELETE FROM suppliers WHERE id = ?", (supplier_id,))
    conn.commit()
    conn.close()
    return "✅ Supplier deleted successfully."

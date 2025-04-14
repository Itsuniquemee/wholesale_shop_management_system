import streamlit as st
import pandas as pd
import models

# Set Page Configuration
st.set_page_config(page_title="Wholesale Shop Management", layout="wide")

# Custom CSS for UI Enhancements
st.markdown(
    """
    <style>
        .big-font { font-size:24px !important; font-weight: bold; text-align: center; }
        .metric-box { 
            padding: 20px; 
            background-color: #000000;
            border-radius: 10px; 
            text-align: center; 
            font-weight: bold;
        }
        .stButton > button { width: 100%; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🛒 Wholesale Shop Management System")

# Sidebar Navigation
menu = ["🏠 Home", "📦 Products", "🚚 Suppliers", "👥 Customers", "📜 Orders", "🛒 Sell"]
choice = st.sidebar.selectbox("Menu", menu)

# Helper function to get customer name by ID
def get_customer_name(customer_id):
    customers = models.get_customers()
    for customer in customers:
        if customer['id'] == customer_id:
            return customer['name']
    return "Unknown"

# Helper function to get supplier name by ID
def get_supplier_name(supplier_id):
    suppliers = models.get_suppliers()
    for supplier in suppliers:
        if supplier['id'] == supplier_id:
            return supplier['name']
    return "Unknown"

# 🏠 Home / Dashboard with Enhanced UI
if choice == "🏠 Home":
    st.markdown("<p class='big-font'>📊 Business Overview</p>", unsafe_allow_html=True)
    
    total_products = len(models.get_products())
    total_suppliers = len(models.get_suppliers())
    total_customers = len(models.get_customers())
    total_orders = len(models.get_orders())

    # Display Summary Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown("<div class='metric-box'><h2>📦</h2><h3>Total Products</h3><p><b>{}</b></p></div>".format(total_products), unsafe_allow_html=True)
    col2.markdown("<div class='metric-box'><h2>🚚</h2><h3>Total Suppliers</h3><p><b>{}</b></p></div>".format(total_suppliers), unsafe_allow_html=True)
    col3.markdown("<div class='metric-box'><h2>👥</h2><h3>Total Customers</h3><p><b>{}</b></p></div>".format(total_customers), unsafe_allow_html=True)
    col4.markdown("<div class='metric-box'><h2>📜</h2><h3>Total Orders</h3><p><b>{}</b></p></div>".format(total_orders), unsafe_allow_html=True)

    st.markdown("---")

    # Product and Supplier Management Sections
    col5, col6 = st.columns(2)

    with col5:
        st.markdown("<p class='big-font'>➕ Add Product</p>", unsafe_allow_html=True)
        with st.form("add_product"):
            name = st.text_input("Product Name")
            
            suppliers = models.get_suppliers()
            if suppliers:
                supplier_options = {f"{s['id']} - {s['name']}": s['id'] for s in suppliers}
                supplier_choice = st.selectbox("Supplier", list(supplier_options.keys()))
                supplier_id = supplier_options[supplier_choice]
            else:
                st.warning("No suppliers available. Please add suppliers first.")
                supplier_id = None
            
            stock = st.number_input("Stock Quantity", min_value=0)
            price = st.number_input("Price", min_value=0.0)
            submitted = st.form_submit_button("Add Product")

            if submitted and supplier_id is not None:
                models.add_product(name, supplier_id, stock, price)
                st.success(f"✅ Product '{name}' added successfully!")
                st.rerun()

    with col6:
        st.markdown("<p class='big-font'>➕ Add Supplier</p>", unsafe_allow_html=True)
        with st.form("add_supplier"):
            name = st.text_input("Supplier Name")
            contact = st.text_input("Contact")
            submitted = st.form_submit_button("Add Supplier")

            if submitted:
                models.add_supplier(name, contact)
                st.success(f"✅ Supplier '{name}' added successfully!")
                st.rerun()

    st.markdown("---")

# 📦 Product Management with Delete Option
elif choice == "📦 Products":
    st.subheader("📦 Product Management")

    products = models.get_products()
    suppliers = models.get_suppliers()

    if products:
        for product in products:
            col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
            col1.text(product["name"])
            col2.text(f"Stock: {product['stock']}")
            col3.text(f"Price: ₹{product['price']}")
            col4.text(f"Supplier: {get_supplier_name(product['supplier_id'])}")
            if col5.button("❌ Delete", key=f"del_prod_{product['id']}"):
                models.delete_product(product['id'])
                st.success(f"Product {product['name']} deleted successfully!")
                st.rerun()

    with st.form("add_product"):
        st.write("➕ Add New Product")
        name = st.text_input("Product Name")
        
        suppliers = models.get_suppliers()
        if suppliers:
            supplier_options = {f"{s['id']} - {s['name']}": s['id'] for s in suppliers}
            supplier_choice = st.selectbox("Supplier", list(supplier_options.keys()))
            supplier_id = supplier_options[supplier_choice]
        else:
            st.warning("No suppliers available. Please add suppliers first.")
            supplier_id = None
        
        stock = st.number_input("Stock Quantity", min_value=0)
        price = st.number_input("Price", min_value=0.0)
        submitted = st.form_submit_button("Add Product")

        if submitted and supplier_id is not None:
            models.add_product(name, supplier_id, stock, price)
            st.success(f"✅ Product '{name}' added successfully!")
            st.rerun()

# 🚚 Supplier Management with Delete Option
elif choice == "🚚 Suppliers":
    st.subheader("🚚 Supplier Management")

    suppliers = models.get_suppliers()

    if suppliers:
        for supplier in suppliers:
            col1, col2, col3 = st.columns([3, 3, 1])
            col1.text(supplier["name"])
            col2.text(supplier["contact"])
            if col3.button("❌ Delete", key=f"del_sup_{supplier['id']}"):
                models.delete_supplier(supplier['id'])
                st.success(f"Supplier {supplier['name']} deleted successfully!")
                st.rerun()

    with st.form("add_supplier"):
        st.write("➕ Add New Supplier")
        name = st.text_input("Supplier Name")
        contact = st.text_input("Contact")
        submitted = st.form_submit_button("Add Supplier")

        if submitted:
            models.add_supplier(name, contact)
            st.success(f"✅ Supplier '{name}' added successfully!")
            st.rerun()

# 👥 Customer Management with Delete Option
elif choice == "👥 Customers":
    st.subheader("👥 Customer Management")

    customers = models.get_customers()

    if customers:
        for customer in customers:
            col1, col2, col3 = st.columns([3, 3, 1])
            col1.text(customer["name"])
            col2.text(customer["contact"])
            if col3.button("❌ Delete", key=f"del_cust_{customer['id']}"):
                models.delete_customer(customer['id'])
                st.success(f"Customer {customer['name']} deleted successfully!")
                st.rerun()

    with st.form("add_customer"):
        st.write("➕ Add New Customer")
        name = st.text_input("Customer Name")
        contact = st.text_input("Contact")
        submitted = st.form_submit_button("Add Customer")

        if submitted:
            models.add_customer(name, contact)
            st.success(f"✅ Customer '{name}' added successfully!")
            st.rerun()

# 📜 Order Management
elif choice == "📜 Orders":
    st.markdown("## 📜 Order Management")
    st.markdown("---")

    orders = models.get_orders()
    customers = models.get_customers()

    if orders:
        for order in orders:
            with st.container():
                st.markdown(
                    f"""
                    <div style="
                        border: 2px solid #3498db; 
                        border-radius: 10px; 
                        padding: 15px; 
                        margin-bottom: 10px; 
                        background-color: #000000;">
                        <strong>🆔 Order ID:</strong> {order['id']}  
                        <br><strong>👥 Customer:</strong> {get_customer_name(order['customer_id'])} (ID: {order['customer_id']})  
                        <br><strong>💰 Total Price:</strong> ₹{order['total_price']}  
                        <br><strong>📅 Date:</strong> {order['date']}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if st.button(f"❌ Delete Order {order['id']}", key=f"delete_order_{order['id']}"):
                    models.delete_order(order["id"])
                    st.success(f"🗑️ Order {order['id']} deleted successfully!")
                    st.rerun()

    else:
        st.info("🚫 No orders found.")

    st.markdown("---")

    # Create new order form
    with st.form("create_order", border=True):
        st.markdown("### ➕ Create New Order")
        
        customers = models.get_customers()
        if customers:
            customer_options = {f"{c['id']} - {c['name']}": c['id'] for c in customers}
            customer_choice = st.selectbox("👤 Select Customer", list(customer_options.keys()))
            customer_id = customer_options[customer_choice]
        else:
            st.warning("No customers available. Please add customers first.")
            customer_id = None
        
        total_price = st.number_input("💵 Total Price (₹)", min_value=0.0, step=0.1)

        if st.form_submit_button("🛒 Place Order", use_container_width=True) and customer_id is not None:
            models.add_order(customer_id, total_price)
            st.success(f"✅ Order placed for {get_customer_name(customer_id)}!")
            st.rerun()

# 🛒 Selling Products
elif choice == "🛒 Sell":
    st.subheader("🛒 Sell Products")

    products = models.get_products()
    customers = models.get_customers()

    if not products or not customers:
        st.warning("⚠️ Ensure you have both products and customers in the system before making a sale.")
    else:
        product_options = {f"{p['id']} - {p['name']} (Stock: {p['stock']})": p['id'] for p in products}
        customer_options = {f"{c['id']} - {c['name']}": c['id'] for c in customers}

        tabs = st.tabs(["🛍️ Sell Product", "📜 Sales History"])

        with tabs[0]:  # Sell Product Tab
            with st.form("sell_product_form"):
                product_choice = st.selectbox("Select Product", list(product_options.keys()))
                customer_choice = st.selectbox("Select Customer", list(customer_options.keys()))
                quantity = st.number_input("Quantity", min_value=1, step=1)
                submit_sell = st.form_submit_button("Sell Product")

                if submit_sell:
                    product_id = product_options[product_choice]
                    customer_id = customer_options[customer_choice]

                    result = models.sell_product(product_id, customer_id, quantity)
                    st.success(result)
                    st.rerun()

        with tabs[1]:  # Sales History Tab
            try:
                sales = models.get_sales()
            except Exception as e:
                sales = []
                st.error(f"Error fetching sales: {e}")

            if not sales:
                st.warning("❌ No sales records found!")
            else:
                st.write("📜 **Sales History**")
                st.table(sales)  # Display as a table

st.sidebar.info("Use the sidebar to navigate between sections.")
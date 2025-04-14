import tkinter as tk
from tkinter import ttk, messagebox
from db import init_db
import models

class WholesaleShopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wholesale Shop Management")
        self.root.geometry("800x500")

        # Initialize Tabs
        self.create_tabs()

    def create_tabs(self):
        tab_control = ttk.Notebook(self.root)

        self.dashboard_tab = ttk.Frame(tab_control)
        self.products_tab = ttk.Frame(tab_control)
        self.customers_tab = ttk.Frame(tab_control)
        self.orders_tab = ttk.Frame(tab_control)
        self.sell_tab = ttk.Frame(tab_control)

        tab_control.add(self.dashboard_tab, text="Dashboard")
        tab_control.add(self.products_tab, text="Products")
        tab_control.add(self.customers_tab, text="Customers")
        tab_control.add(self.orders_tab, text="Orders")
        tab_control.add(self.sell_tab, text="Sell")

        tab_control.pack(expand=1, fill="both")

        # Initialize each section
        self.create_dashboard_tab()
        self.create_products_tab()
        self.create_customers_tab()
        self.create_sell_tab()

    def create_dashboard_tab(self):
        ttk.Label(self.dashboard_tab, text="Dashboard: Summary Statistics", font=("Arial", 14)).pack(pady=20)

    def create_products_tab(self):
        ttk.Label(self.products_tab, text="Product Management", font=("Arial", 12)).pack(pady=10)

        self.product_list = ttk.Treeview(self.products_tab, columns=("ID", "Name", "Stock", "Price"), show="headings")
        self.product_list.heading("ID", text="ID")
        self.product_list.heading("Name", text="Name")
        self.product_list.heading("Stock", text="Stock")
        self.product_list.heading("Price", text="Price")
        self.product_list.pack(pady=10, fill="both", expand=True)
        self.load_products()

        ttk.Button(self.products_tab, text="Add Product", command=self.show_add_product_dialog).pack(pady=5)

    def load_products(self):
        for row in self.product_list.get_children():
            self.product_list.delete(row)

        products = models.get_products()
        for product in products:
            self.product_list.insert("", "end", values=(product["id"], product["name"], product["stock"], product["price"]))

    def show_add_product_dialog(self):
        add_product_window = tk.Toplevel(self.root)
        add_product_window.title("Add Product")
        add_product_window.geometry("300x200")

        ttk.Label(add_product_window, text="Name:").pack(pady=5)
        name_entry = ttk.Entry(add_product_window)
        name_entry.pack(pady=5)

        ttk.Label(add_product_window, text="Stock:").pack(pady=5)
        stock_entry = ttk.Entry(add_product_window)
        stock_entry.pack(pady=5)

        ttk.Label(add_product_window, text="Price:").pack(pady=5)
        price_entry = ttk.Entry(add_product_window)
        price_entry.pack(pady=5)

        def save_product():
            name = name_entry.get()
            stock = stock_entry.get()
            price = price_entry.get()

            if not name or not stock or not price:
                messagebox.showerror("Error", "All fields are required!")
                return

            models.add_product(name, int(stock), float(price))
            self.load_products()
            add_product_window.destroy()
            messagebox.showinfo("Success", "Product added successfully!")

        ttk.Button(add_product_window, text="Save", command=save_product).pack(pady=10)

    def create_customers_tab(self):
        ttk.Label(self.customers_tab, text="Customer Management", font=("Arial", 12)).pack(pady=10)

        self.customer_list = ttk.Treeview(self.customers_tab, columns=("ID", "Name", "Contact", "Action"), show="headings")
        self.customer_list.heading("ID", text="ID")
        self.customer_list.heading("Name", text="Name")
        self.customer_list.heading("Contact", text="Contact")
        self.customer_list.heading("Action", text="Action")  # Placeholder for delete button

        self.customer_list.pack(pady=10, fill="both", expand=True)
        self.load_customers()

        ttk.Button(self.customers_tab, text="Add Customer", command=self.show_add_customer_dialog).pack(pady=5)

    def load_customers(self):
        """Loads customers into the customer list"""
        for row in self.customer_list.get_children():
            self.customer_list.delete(row)

        customers = models.get_customers()
        for customer in customers:
            self.customer_list.insert("", "end", values=(customer["id"], customer["name"], customer["contact"], "🗑️ Delete"))

        # Bind delete functionality
        self.customer_list.bind("<Double-1>", self.handle_customer_deletion)

    def handle_customer_deletion(self, event):
        """Handles the deletion of a selected customer"""
        selected_item = self.customer_list.selection()
        if not selected_item:
            return

        customer_id = self.customer_list.item(selected_item, "values")[0]
        customer_name = self.customer_list.item(selected_item, "values")[1]

        confirm = messagebox.askyesno("Delete Customer", f"Are you sure you want to delete '{customer_name}'?")
        if confirm:
            models.delete_customer(customer_id)
            messagebox.showinfo("Success", f"Customer '{customer_name}' deleted successfully!")
            self.load_customers()  # Refresh customer list

    def show_add_customer_dialog(self):
        add_customer_window = tk.Toplevel(self.root)
        add_customer_window.title("Add Customer")
        add_customer_window.geometry("300x200")

        ttk.Label(add_customer_window, text="Name:").pack(pady=5)
        name_entry = ttk.Entry(add_customer_window)
        name_entry.pack(pady=5)

        ttk.Label(add_customer_window, text="Contact:").pack(pady=5)
        contact_entry = ttk.Entry(add_customer_window)
        contact_entry.pack(pady=5)

        def save_customer():
            name = name_entry.get()
            contact = contact_entry.get()

            if not name or not contact:
                messagebox.showerror("Error", "All fields are required!")
                return

            models.add_customer(name, contact)
            self.load_customers()
            add_customer_window.destroy()
            messagebox.showinfo("Success", "Customer added successfully!")

        ttk.Button(add_customer_window, text="Save", command=save_customer).pack(pady=10)

    def create_sell_tab(self):
        """Creates the Sell Tab UI"""
        ttk.Label(self.sell_tab, text="Sell Products", font=("Arial", 14)).pack(pady=10)

        products = models.get_products()
        customers = models.get_customers()

        if not products or not customers:
            ttk.Label(self.sell_tab, text="⚠️ Add products and customers before making sales.").pack(pady=10)
            return

        self.product_map = {f"{p['id']} - {p['name']} (Stock: {p['stock']})": p['id'] for p in products}
        self.customer_map = {f"{c['id']} - {c['name']}": c['id'] for c in customers}

        self.product_var = tk.StringVar()
        self.customer_var = tk.StringVar()
        self.quantity_var = tk.IntVar(value=1)

        ttk.Label(self.sell_tab, text="Select Product:").pack(pady=5)
        self.product_dropdown = ttk.Combobox(self.sell_tab, textvariable=self.product_var, values=list(self.product_map.keys()), state="readonly")
        self.product_dropdown.pack(pady=5)

        ttk.Label(self.sell_tab, text="Select Customer:").pack(pady=5)
        self.customer_dropdown = ttk.Combobox(self.sell_tab, textvariable=self.customer_var, values=list(self.customer_map.keys()), state="readonly")
        self.customer_dropdown.pack(pady=5)

        ttk.Label(self.sell_tab, text="Quantity:").pack(pady=5)
        self.quantity_entry = ttk.Entry(self.sell_tab, textvariable=self.quantity_var)
        self.quantity_entry.pack(pady=5)

        ttk.Button(self.sell_tab, text="Sell Product", command=self.process_sale).pack(pady=10)

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = WholesaleShopApp(root)
    root.mainloop()

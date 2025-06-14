import tkinter as tk
from tkinter import ttk, messagebox

products = []
edit_index = -1
dark_mode = False

def format_product(name, price, quantity):
    return (name, f"Rs. {price:.2f}", f"{quantity}")

def refresh_table():
    tree.delete(*tree.get_children())
    for i, (name, price, quantity) in enumerate(products):
        tree.insert('', 'end', values=format_product(name, price, quantity), tags=('low',) if quantity < 5 else '')

def add_or_update_product(event=None):
    global edit_index
    name = name_entry.get().strip()
    try:
        price = float(price_entry.get())
        quantity = int(quantity_entry.get())
    except ValueError:
        status_var.set("Invalid price or quantity.")
        return

    if not name:
        status_var.set("Product name is required.")
        return

    if edit_index != -1:
        products[edit_index] = (name, price, quantity)
        status_var.set("Product updated.")
        add_button.config(text="Add Product")
        edit_index = -1
    else:
        products.append((name, price, quantity))
        status_var.set("Product added.")

    clear_fields()
    refresh_table()
    filter_products()

def edit_product(event=None):
    global edit_index
    selected = tree.selection()
    if not selected:
        return
    index = tree.index(selected[0])
    name, price, quantity = products[index]
    name_entry.delete(0, tk.END)
    name_entry.insert(0, name)
    price_entry.delete(0, tk.END)
    price_entry.insert(0, str(price))
    quantity_entry.delete(0, tk.END)
    quantity_entry.insert(0, str(quantity))
    add_button.config(text="Update Product")
    edit_index = index
    status_var.set("Editing product...")

def delete_product(event=None):
    global edit_index
    selected = tree.selection()
    if not selected:
        return
    index = tree.index(selected[0])
    products.pop(index)
    refresh_table()
    status_var.set("Product deleted.")
    clear_fields()
    add_button.config(text="Add Product")
    edit_index = -1

def clear_fields():
    name_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)

def clear_all():
    if messagebox.askyesno("Confirm", "Delete all products?"):
        products.clear()
        refresh_table()
        clear_fields()
        add_button.config(text="Add Product")
        status_var.set("All products cleared.")

def copy_product():
    selected = tree.selection()
    if not selected:
        return
    item = tree.item(selected[0])['values']
    root.clipboard_clear()
    root.clipboard_append(', '.join(item))
    status_var.set("Copied to clipboard.")

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    bg = "#2e2e2e" if dark_mode else "#f0f0f0"
    fg = "#ffffff" if dark_mode else "#000000"
    root.configure(bg=bg)
    for widget in root.winfo_children():
        try:
            widget.configure(bg=bg, fg=fg)
        except:
            pass
    for child in input_frame.winfo_children():
        try:
            child.configure(bg=bg, fg=fg)
        except:
            pass
    tree.tag_configure('low', background="#ffcccc" if not dark_mode else "#662222")

def filter_products(event=None):
    query = search_var.get().lower()
    tree.delete(*tree.get_children())
    for name, price, quantity in products:
        if query in name.lower():
            tree.insert('', 'end', values=format_product(name, price, quantity), tags=('low',) if quantity < 5 else '')

def sort_by_column(col):
    col_index = {"Name": 0, "Price": 1, "Quantity": 2}[col]
    is_desc = tree.heading(col, option="text").endswith("↓")
    products.sort(key=lambda x: x[col_index], reverse=not is_desc)
    for c in columns:
        arrow = "↓" if c == col and not is_desc else "↑" if c == col else ""
        tree.heading(c, text=c + " " + arrow)
    refresh_table()

# UI Setup
root = tk.Tk()
root.title("SmartShop")
root.geometry("800x600")
root.configure(bg="#f0f0f0")


# Variables
search_var = tk.StringVar()
status_var = tk.StringVar()

# Title
tk.Label(root, text="🛒 Product Manager", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=10)

# Search
search_frame = tk.Frame(root, bg="#f0f0f0")
search_frame.pack()
tk.Label(search_frame, text="🔍 Search:", bg="#f0f0f0").pack(side=tk.LEFT)
search_entry = tk.Entry(search_frame, textvariable=search_var)
search_entry.pack(side=tk.LEFT, padx=5)
search_entry.bind("<KeyRelease>", filter_products)

# Input Form
input_frame = tk.Frame(root, bg="#f0f0f0")
input_frame.pack(pady=10)

tk.Label(input_frame, text="Product Name:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
tk.Label(input_frame, text="Price:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
tk.Label(input_frame, text="Quantity:", bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5)

name_entry = tk.Entry(input_frame)
price_entry = tk.Entry(input_frame)
quantity_entry = tk.Entry(input_frame)

name_entry.grid(row=0, column=1, padx=5, pady=5)
price_entry.grid(row=1, column=1, padx=5, pady=5)
quantity_entry.grid(row=2, column=1, padx=5, pady=5)

for entry in (name_entry, price_entry, quantity_entry):
    entry.bind("<Return>", add_or_update_product)
    entry.bind("<Shift-Return>", add_or_update_product)

# Buttons
add_button = tk.Button(root, text="Add Product", command=add_or_update_product, bg="#28a745", fg="white", width=20)
add_button.pack(pady=5)

action_frame = tk.Frame(root, bg="#f0f0f0")
action_frame.pack(pady=5)
tk.Button(action_frame, text="✏️ Edit", command=edit_product, bg="#007BFF", fg="white", width=10).pack(side=tk.LEFT, padx=5)
tk.Button(action_frame, text="🗑️ Delete", command=delete_product, bg="#dc3545", fg="white", width=10).pack(side=tk.LEFT, padx=5)
tk.Button(action_frame, text="🧹 Clear All", command=clear_all, bg="#6c757d", fg="white", width=10).pack(side=tk.LEFT, padx=5)
tk.Button(action_frame, text="📋 Copy", command=copy_product, bg="#17a2b8", fg="white", width=10).pack(side=tk.LEFT, padx=5)
tk.Button(action_frame, text="🌗 Theme", command=toggle_theme, bg="#333", fg="white", width=10).pack(side=tk.LEFT, padx=5)

# Table
columns = ["Name", "Price", "Quantity"]
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col + " ↓", command=lambda c=col: sort_by_column(c))
    tree.column(col, width=200, anchor="center")
tree.pack(pady=10)
tree.bind("<Delete>", delete_product)
tree.tag_configure('low', background="#ffcccc")

# Status Bar
status_bar = tk.Frame(root, bg="#dddddd", relief="sunken", bd=1)
status_bar.pack(fill="x", side="bottom")
status_label = tk.Label(status_bar, textvariable=status_var, anchor="w", bg="#dddddd")
status_label.pack(fill="x")

# Keyboard Shortcuts
root.bind("<Control-e>", edit_product)
root.bind("<Control-d>", delete_product)
root.bind("<Control-Shift-C>", lambda e: copy_product())

root.mainloop()

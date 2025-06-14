import tkinter as tk
from tkinter import ttk, messagebox, Menu
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SmartShop App")
        self.geometry("800x600")
        

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for Page in (LoginPage, ProductPage, AnalysisPage):
            frame = Page(parent=container, controller=self)
            self.frames[Page] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(LoginPage)

    def show_frame(self, page_class):
        self.frames[page_class].tkraise()
        # Show menu only on Product & Analysis pages
        if page_class in (ProductPage, AnalysisPage):
            self.config(menu=self.frames[ProductPage].menubar)
        else:
            self.config(menu=None)

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="🔐 SmartShop Login", font=("Arial", 18)).pack(pady=20)
        self.user = tk.Entry(self, width=30)
        self.user.pack(pady=5)
        self.pwd = tk.Entry(self, show="*", width=30)
        self.pwd.pack(pady=5)
        tk.Button(self, text="Sign in", width=20, command=self.login).pack(pady=20)

    def login(self):
        if self.user.get() == "admin" and self.pwd.get() == "1234":
            self.user.delete(0, tk.END)
            self.pwd.delete(0, tk.END)
            self.controller.show_frame(ProductPage)
        else:
            messagebox.showerror("Invalid", "Wrong credentials")

class ProductPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.products = []
        self.edit_index = None

        # Menu bar for this page
        self.menubar = Menu(controller)
        menu = Menu(self.menubar, tearoff=False)
        menu.add_command(label="Product Manager", command=lambda: controller.show_frame(ProductPage))
        menu.add_command(label="Analysis", command=lambda: controller.show_frame(AnalysisPage))
        menu.add_command(label="Logout", command=lambda: controller.show_frame(LoginPage))
        self.menubar.add_cascade(label="Menu", menu=menu)

        tk.Label(self, text="🛒 Product Manager", font=("Arial", 20)).pack(pady=10)

        self.search_var = tk.StringVar()
        sf = tk.Frame(self); sf.pack()
        tk.Label(sf, text="Search:").pack(side=tk.LEFT)
        tk.Entry(sf, textvariable=self.search_var).pack(side=tk.LEFT, padx=5)
        self.search_var.trace_add("write", lambda *a: self.refresh_table())

        cols = ("Name", "Price", "Qty")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree.heading(c, text=c, command=lambda c=c: self.sort_by(c))
            self.tree.column(c, width=180, anchor="center")
        self.tree.pack(pady=10)
        self.tree.bind("<Double-1>", lambda e: self.start_edit())

        form = tk.Frame(self); form.pack(pady=5)
        for i, lbl in enumerate(("Name:", "Price:", "Quantity:")):
            tk.Label(form, text=lbl).grid(row=i, column=0, padx=5)
        self.name = tk.Entry(form); self.price = tk.Entry(form); self.qty = tk.Entry(form)
        self.name.grid(row=0, column=1); self.price.grid(row=1, column=1); self.qty.grid(row=2, column=1)

        bf = tk.Frame(self); bf.pack(pady=5)
        tk.Button(bf, text="Add", bg="#28a745", fg="white", width=12, command=self.add).grid(row=0, column=0, padx=5)
        tk.Button(bf, text="Edit", bg="#007BFF", fg="white", width=12, command=self.start_edit).grid(row=0, column=1, padx=5)
        tk.Button(bf, text="Delete", bg="#dc3545", fg="white", width=12, command=self.delete).grid(row=0, column=2, padx=5)
        tk.Button(bf, text="Clear All", width=12, command=self.clear_all).grid(row=0, column=3, padx=5)

    def refresh_table(self):
        q = self.search_var.get().lower()
        self.tree.delete(*self.tree.get_children())
        for i, (n,p,qty) in enumerate(self.products):
            if q in n.lower():
                self.tree.insert("", "end", iid=i, values=(n, f"₹{p:.2f}", qty))

    def add(self):
        try:
            n = self.name.get().strip()
            p = float(self.price.get())
            qty = int(self.qty.get())
            if not n: raise ValueError("Name required")
        except Exception as e:
            messagebox.showwarning("Input Error", e); return
        if self.edit_index is None:
            self.products.append((n, p, qty))
        else:
            self.products[self.edit_index] = (n, p, qty)
            self.edit_index = None
        self.clear_form(); self.refresh_table()

    def start_edit(self):
        sel = self.tree.selection()
        if sel:
            i = int(sel[0]); n,p,qty = self.products[i]
            self.name.delete(0,'end'); self.name.insert(0, n)
            self.price.delete(0,'end'); self.price.insert(0, str(p))
            self.qty.delete(0,'end'); self.qty.insert(0, str(qty))
            self.edit_index = i

    def delete(self):
        sel = self.tree.selection()
        if sel:
            del self.products[int(sel[0])]; self.refresh_table()

    def clear_all(self):
        if messagebox.askyesno("Confirm", "Clear all?"):
            self.products.clear(); self.refresh_table()

    def clear_form(self):
        for e in (self.name, self.price, self.qty):
            e.delete(0, 'end')

    def sort_by(self, col):
        idx = {"Name":0,"Price":1,"Qty":2}[col]
        self.products.sort(key=lambda x: x[idx])
        self.refresh_table()

class AnalysisPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.product_page = controller.frames[ProductPage]
        tk.Label(self, text="📈 Price Analysis", font=("Arial", 20)).pack(pady=10)
        tk.Button(self, text="Refresh Chart", command=self.display_chart).pack(pady=5)
        self.chart_area = tk.Frame(self)
        self.chart_area.pack(fill="both", expand=True)
        self.display_chart()

    def display_chart(self):
        for w in self.chart_area.winfo_children():
            w.destroy()
        data = self.product_page.products
        names = [n for n,_,_ in data]
        prices = [p for _,p,_ in data]
        fig = Figure(figsize=(6,4), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(names, prices, color="skyblue")
        ax.set_ylabel("Price (₹)")
        ax.set_title("Product Price Analysis")
        for i, v in enumerate(prices):
            ax.text(i, v, f"{v:.2f}", ha="center", va="bottom")
        canvas = FigureCanvasTkAgg(fig, master=self.chart_area)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# ───────────────────────────────────────────────
# 1️⃣ Define all your pages (subclasses of tk.Frame)
# ───────────────────────────────────────────────

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Please Log In", font=("Arial", 18)).pack(pady=20)
        self.user = tk.Entry(self)
        self.user.pack(pady=5)
        self.pwd = tk.Entry(self, show="*")
        self.pwd.pack(pady=5)
        tk.Button(self, text="Sign in", command=self.login).pack(pady=10)

    def login(self):
        username = self.user.get()
        password = self.pwd.get()
        if username == "admin" and password == "1234":
            self.controller.show_frame(AppPage)
        else:
            messagebox.showerror("Invalid", "Wrong username or password")

class AppPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Button(self, text="Logout",
                  command=lambda: controller.show_frame(LoginPage)).pack(pady=5)
        tk.Label(self, text="🛒 Product Manager",
                 font=("Arial", 20, "bold")).pack(pady=10)
        # insert your product manager UI here
        self.tree = ttk.Treeview(self, columns=("Name", "Price", "Qty"), show="headings")
        for col in ("Name", "Price", "Qty"):
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

# ───────────────────────────────────────────────
# 2️⃣ Controller: initialize pages and manage switching
# ───────────────────────────────────────────────

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
        for Page in (LoginPage, AppPage):
            page = Page(parent=container, controller=self)
            self.frames[Page] = page
            page.grid(row=0, column=0, sticky="nsew")

        # Start on LoginPage
        self.show_frame(LoginPage)

    def show_frame(self, page_class):
        self.frames[page_class].tkraise()

# ───────────────────────────────────────────────
# 3️⃣ Run the application
# ───────────────────────────────────────────────
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
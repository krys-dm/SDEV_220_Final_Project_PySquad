import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

# --- Database Setup ---
DB_FILE = "pizzapy.db"

def init_database():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            remember_me INTEGER DEFAULT 0
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            description TEXT,
            total_price REAL
        )
    ''')
    conn.commit()
    conn.close()

init_database()

# --- Login Window ---
class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PizzaPy Login")
        self.geometry("400x500")
        self.configure(bg="#1E1E1E")

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.remember_var = tk.IntVar()

        self.create_widgets()
        self.check_remembered_user()

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TLabel", background="#1E1E1E", foreground="#CCCCCC")
        style.configure("TButton", background="#212733", foreground="white")

        # Welcome Label
        tk.Label(self, text="Welcome to PizzaPy!", font=("Arial", 20, "bold"),
                 bg="#1E1E1E", fg="white").pack(pady=(20, 20))

        # Username
        ttk.Label(self, text="Username:").pack(pady=(5, 5))
        self.username_entry = tk.Entry(self, textvariable=self.username_var,
                                       bg="#2C2C2C", fg="white", insertbackground="white",
                                       highlightbackground="#3C3F41", highlightthickness=1, bd=1, relief="solid")
        self.username_entry.pack(pady=(0, 10))

        # Password
        ttk.Label(self, text="Password:").pack(pady=(5, 5))
        self.password_entry = tk.Entry(self, textvariable=self.password_var, show="*",
                                       bg="#2C2C2C", fg="white", insertbackground="white",
                                       highlightbackground="#3C3F41", highlightthickness=1, bd=1, relief="solid")
        self.password_entry.pack(pady=(0, 10))

        # Remember Me
        self.remember_checkbox = tk.Checkbutton(self, text="Remember Me", variable=self.remember_var,
                                                 bg="#1E1E1E", fg="white", activebackground="#1E1E1E",
                                                 activeforeground="white", selectcolor="#1E1E1E")
        self.remember_checkbox.pack(pady=(5, 10))

        # Login / Sign Up Buttons
        button_frame = tk.Frame(self, bg="#1E1E1E")
        button_frame.pack(pady=10)

        self.button_style = {
            "bg": "#212733",
            "fg": "white",
            "activebackground": "#3A9BDC",
            "activeforeground": "white",
            "highlightbackground": "#3C3F41",
            "highlightthickness": 1,
            "bd": 1,
            "relief": "solid",
            "width": 15
        }

        tk.Button(button_frame, text="Login", command=self.login_user, **self.button_style).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Sign Up", command=self.signup_user, **self.button_style).grid(row=0, column=1, padx=5)

        # Divider
        tk.Label(self, text="──────────  OR  ──────────", bg="#1E1E1E", fg="#CCCCCC").pack(pady=10)

        # Menu / Guest Buttons
        guest_frame = tk.Frame(self, bg="#1E1E1E")
        guest_frame.pack(pady=5)

        tk.Button(guest_frame, text="Menu", command=lambda: self.launch_pizzapy(self.username_var.get() or "Guest"),
                  **self.button_style).grid(row=0, column=0, padx=5)
        tk.Button(guest_frame, text="Continue as Guest", command=lambda: self.launch_pizzapy("Guest"),
                  **self.button_style).grid(row=0, column=1, padx=5)

    def check_remembered_user(self):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE remember_me=1")
        result = c.fetchone()
        conn.close()

        if result:
            username = result[0]
            self.launch_pizzapy(username)

    def login_user(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()

        if user:
            if self.remember_var.get():
                c.execute("UPDATE users SET remember_me=1 WHERE username=?", (username,))
            else:
                c.execute("UPDATE users SET remember_me=0 WHERE username=?", (username,))
            conn.commit()
            conn.close()

            self.launch_pizzapy(username)
        else:
            conn.close()
            messagebox.showerror("Error", "Incorrect username or password.")

    def signup_user(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if not username or not password:
            messagebox.showwarning("Warning", "Username and password cannot be empty.")
            return

        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Account created successfully! You can now log in.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already taken.")
        finally:
            conn.close()

    def launch_pizzapy(self, username):
        self.destroy()
        os.system(f'python pizzapy_gui.py "{username}"')  # Pass username into GUI

if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()

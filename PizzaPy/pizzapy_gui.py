import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import sys

# Menu Data 
specialty_pizzas = {
    "Margherita": {"Sauce": "tomato", "Cheese": "mozzarella slices", "Toppings": ["fresh basil", "olive oil", "tomatoes"], "Price": 15.00},
    "Pepperoni": {"Sauce": "tomato", "Cheese": "mozzarella", "Toppings": ["pepperoni"], "Price": 15.00},
    "Hawaiian": {"Sauce": "tomato", "Cheese": "mozzarella", "Toppings": ["ham", "pineapple"], "Price": 15.00},
    "Meat Lovers": {"Sauce": "tomato", "Cheese": "mozzarella", "Toppings": ["pepperoni", "sausage", "ham", "bacon"], "Price": 15.00},
    "Veggie": {"Sauce": "tomato", "Cheese": "mozzarella", "Toppings": ["bell peppers", "onions", "mushrooms", "olives", "spinach"], "Price": 15.00},
    "BBQ Chicken": {"Sauce": "bbq", "Cheese": "mozzarella", "Toppings": ["grilled chicken", "red onions", "cilantro"], "Price": 15.00},
    "Buffalo Chicken": {"Sauce": "buffalo", "Cheese": "mozzarella", "Toppings": ["spicy chicken", "red onions", "ranch drizzle"], "Price": 15.00},
    "Cheese": {"Sauce": "tomato", "Cheese": "mozzarella", "Toppings": ["Cheese"], "Price": 15.00}
}

sauces = ["tomato", "bbq", "buffalo"]
cheeses = ["mozzarella", "mozzarella slices"]
proteins = ["pepperoni", "ham", "sausage", "bacon", "grilled chicken", "spicy chicken"]
veggies = ["fresh basil", "olive oil", "tomatoes", "pineapple", "bell peppers", "onions", "mushrooms", "olives", "spinach", "red onions", "cilantro", "ranch drizzle"]

class PizzaApp(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.title(f"PizzaPy - Welcome, {self.username}")
        self.geometry("700x900")
        self.configure(bg="#1E1E1E")
        self.cart = []

        canvas = tk.Canvas(self, bg="#1E1E1E", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1E1E1E")
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.main_frame = tk.Frame(scrollable_frame, bg="#1E1E1E")
        self.main_frame.pack(anchor="center")

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TFrame", background="#1E1E1E")
        style.configure("TLabelframe", background="#1E1E1E", foreground="white")
        style.configure("TLabelframe.Label", background="#1E1E1E", foreground="white", font=('Arial', 12, 'bold'))
        style.configure("TLabel", background="#1E1E1E", foreground="#CCCCCC")
        style.configure("TCombobox", fieldbackground="#2C2C2C", foreground="white", background="#2C2C2C")

        self.button_style = {
            "bg": "#212733",
            "fg": "white",
            "activebackground": "#3A9BDC",
            "activeforeground": "white",
            "highlightbackground": "#3C3F41",
            "highlightthickness": 1,
            "bd": 1,
            "relief": "solid",
            "width": 20
        }

        # Header
        tk.Label(self.main_frame, text="PizzaPy Menu!", font=("Arial", 20, "bold"), bg="#1E1E1E", fg="white").pack(pady=(10, 20))

        # Name entry
        name_frame = ttk.Frame(self.main_frame)
        name_frame.pack(fill="x", padx=15, pady=10)
        ttk.Label(name_frame, text="Customer Name:").pack(side="left", padx=5)
        self.name_entry = tk.Entry(name_frame, bg="#2C2C2C", fg="white", insertbackground="white")
        self.name_entry.pack(side="left", fill="x", expand=True)
        self.name_entry.insert(0, self.username)

        # Specialty pizzas
        specialty_frame = ttk.LabelFrame(self.main_frame, text="Specialty Pizzas")
        specialty_frame.pack(fill="x", padx=15, pady=10)
        self.specialty_listbox = tk.Listbox(specialty_frame, width=80, height=10, bg="#2C2C2C", fg="white",
                                            highlightbackground="#3C3F41", selectbackground="#3A9BDC", selectforeground="black")
        for pizza, details in specialty_pizzas.items():
            toppings = ", ".join(details["Toppings"]) or "No Toppings"
            self.specialty_listbox.insert(tk.END, f"{pizza} (${details['Price']:.2f}) - {toppings}")
        self.specialty_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        tk.Button(specialty_frame, text="Add Specialty Pizza", command=self.add_specialty_to_cart, **self.button_style).pack(pady=5)

        # Build your own section
        build_frame = ttk.LabelFrame(self.main_frame, text="Build Your Own")
        build_frame.pack(padx=40, pady=10, fill="x", anchor="center")

        tk.Label(build_frame, text="Starts at $10 - $1 per selected topping", bg="#1E1E1E", fg="white", justify="center").grid(
            row=0, column=0, pady=(0, 10), sticky="w")

        # Custom Name
        tk.Label(build_frame, text="Custom Name:", bg="#1E1E1E", fg="white").grid(row=1, column=0, sticky="w", padx=10)
        self.custom_name_entry = tk.Entry(build_frame, bg="#2C2C2C", fg="white", insertbackground="white")
        self.custom_name_entry.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))

        # Sauce
        tk.Label(build_frame, text="Sauce:", bg="#1E1E1E", fg="white").grid(row=3, column=0, sticky="w", padx=10)
        self.sauce_var = tk.StringVar(value=sauces[0])
        sauce_menu = ttk.Combobox(build_frame, textvariable=self.sauce_var, values=sauces)
        sauce_menu.grid(row=4, column=0, sticky="ew", padx=10, pady=(0, 10))

        # Cheese
        tk.Label(build_frame, text="Cheese:", bg="#1E1E1E", fg="white").grid(row=5, column=0, sticky="w", padx=10)
        self.cheese_var = tk.StringVar(value=cheeses[0])
        cheese_menu = ttk.Combobox(build_frame, textvariable=self.cheese_var, values=cheeses)
        cheese_menu.grid(row=6, column=0, sticky="ew", padx=10, pady=(0, 10))

        # Toppings Frame
        toppings_frame = ttk.Frame(build_frame)
        toppings_frame.grid(row=7, column=0, pady=(5, 10), sticky="ew", padx=10)
        toppings_frame.columnconfigure(0, weight=1)
        toppings_frame.columnconfigure(1, weight=1)

        self.protein_listbox = tk.Listbox(toppings_frame, selectmode="multiple", exportselection=False, height=6, bg="#2C2C2C", fg="white")
        for p in proteins:
            self.protein_listbox.insert(tk.END, p)
        self.protein_listbox.grid(row=0, column=0, padx=5, sticky="ew")

        self.veggie_listbox = tk.Listbox(toppings_frame, selectmode="multiple", exportselection=False, height=6, bg="#2C2C2C", fg="white")
        for v in veggies:
            self.veggie_listbox.insert(tk.END, v)
        self.veggie_listbox.grid(row=0, column=1, padx=5, sticky="ew")

        # Selected toppings
        self.selected_toppings_label = tk.Label(build_frame, text="Selected Toppings:", bg="#1E1E1E", fg="white")
        self.selected_toppings_label.grid(row=8, column=0, pady=5, sticky="w", padx=10)

        # Add custom pizza button
        tk.Button(build_frame, text="Add Custom Pizza", command=self.add_custom_to_cart,
                bg="#3A9BDC", fg="white").grid(row=9, column=0, pady=10, sticky="ew", padx=10)

        # Cart
        cart_frame = ttk.LabelFrame(self.main_frame, text="Your Order")
        cart_frame.pack(fill="both", expand=True, padx=15, pady=10)
        self.cart_text = tk.Text(cart_frame, height=10, wrap="word", bg="#2C2C2C", fg="white", state=tk.DISABLED)
        self.cart_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Tip Buttons
        tip_button_frame = ttk.Frame(self.main_frame)
        tip_button_frame.pack(pady=(0, 5))
        
        ttk.Label(tip_button_frame, text="Add Tip (%):").pack(side="left", padx=(0, 10))
        for percent in [15, 20, 25]:
            ttk.Button(tip_button_frame, text=f"{percent}%", command=lambda p=percent: self.set_tip_percent(p)).pack(side="left", padx=5)

        # Total Label
        self.total_label = tk.Label(self.main_frame, text="Subtotal: $0.00 | Tax: $0.00 | Tip: $0.00 | Total: $0.00",
                                    font=("Arial", 14), bg="#1E1E1E", fg="white")
        self.total_label.pack(pady=5)

        self.tip_percent = 0 

        # Buttons
        button_frame = tk.Frame(self.main_frame, bg="#1E1E1E")
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Checkout", command=self.checkout, **self.button_style).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Save Order to Database", command=self.save_order, **self.button_style).grid(row=0, column=1, padx=10)


    def update_selected_toppings_display(self, event=None):
        proteins = [self.protein_listbox.get(i) for i in self.protein_listbox.curselection()]
        veggies = [self.veggie_listbox.get(i) for i in self.veggie_listbox.curselection()]
        all_toppings = proteins + veggies
        self.selected_toppings_label.config(text="Selected Toppings: " + ", ".join(all_toppings))

    def add_specialty_to_cart(self):
        selected = self.specialty_listbox.curselection()
        if selected:
            name = list(specialty_pizzas.keys())[selected[0]]
            price = specialty_pizzas[name]['Price']
            self.cart.append((name, price))
            self.update_cart()

    def add_custom_to_cart(self):
        sauce = self.sauce_var.get()
        cheese = self.cheese_var.get()
        name = self.custom_name_entry.get().strip() or "Custom Pizza"
        toppings = [self.protein_listbox.get(i) for i in self.protein_listbox.curselection()] + \
                   [self.veggie_listbox.get(i) for i in self.veggie_listbox.curselection()]
        description = f"{name} ({sauce} sauce, {cheese} cheese, {', '.join(toppings)})"
        price = 10 + len(toppings) * 1
        self.cart.append((description, price))
        self.update_cart()

    def remove_item(self):
        selection = self.cart_listbox.curselection()
        if selection:
            del self.cart[selection[0]]
            self.update_cart()

    def update_cart(self):
        subtotal = sum(price for _, price in self.cart)
        tax = subtotal * 0.06
        tip = subtotal * (self.tip_percent / 100)
        total = subtotal + tax + tip

        # Update cart display
        self.cart_text.configure(state=tk.NORMAL)
        self.cart_text.delete(1.0, tk.END)
        for item, price in self.cart:
            self.cart_text.insert(tk.END, f"{item} - ${price:.2f}\n")
        self.cart_text.configure(state=tk.DISABLED)

        self.total_label.config(text=f"Subtotal: ${subtotal:.2f} | Tax: ${tax:.2f} | Tip: ${tip:.2f} | Total: ${total:.2f}")


    def checkout(self):
        if not self.cart:
            messagebox.showwarning("Cart Empty", "Add items to your cart first.")
            return
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Missing Name", "Please enter your name.")
            return
        items = "\n".join([f"{i} - ${p:.2f}" for i, p in self.cart])
        subtotal = sum(p for _, p in self.cart)
        tax = subtotal * 0.06
        tip = subtotal * (self.tip_percent / 100)
        total = subtotal + tax + tip
        messagebox.showinfo("Receipt", f"Customer: {name}\n\n{items}\n\nSubtotal: ${subtotal:.2f}\nTax: ${tax:.2f}\nTip: ${tip:.2f}\nTotal: ${total:.2f}")
        self.cart.clear()
        self.update_cart()

    def save_order(self):
        if not self.cart:
            messagebox.showwarning("Cart Empty", "Add items before saving.")
            return
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Missing Name", "Please enter your name.")
            return
        desc = "; ".join(i for i, _ in self.cart)
        subtotal = sum(p for _, p in self.cart)
        tax = subtotal * 0.06
        tip = subtotal * (self.tip_percent / 100)
        total = subtotal + tax + tip
        try:
            conn = sqlite3.connect("pizzapy.db")
            cur = conn.cursor()
            cur.execute("INSERT INTO orders (customer_name, description, total_price) VALUES (?, ?, ?)", (name, desc, total))
            conn.commit()
            conn.close()
            messagebox.showinfo("Saved", "Order saved!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def set_tip_percent(self, percent):
        self.tip_percent = percent
        self.update_cart()


# Run App
if __name__ == "__main__":
    user = sys.argv[1] if len(sys.argv) > 1 else "Guest"
    PizzaApp(user).mainloop()

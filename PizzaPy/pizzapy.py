import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# --- Menu Data ---
specialty_pizzas = {
    "Margherita": {"Sauce": "tomato", "Cheese": "mozzarella slices", "Toppings": ["fresh basil", "olive oil", "tomatoes"], "Price": 15.00},
    "Pepperoni": {"Sauce": "tomato", "Cheese": "mozzarella", "Toppings": ["pepperoni"], "Price": 15.00},
    "Hawaiian": {"Sauce": "tomato", "Cheese": "mozzarella", "Toppings": ["ham", "pineapple"], "Price": 15.00},
    "Meat Lovers": {"Sauce": "tomato", "Cheese": "mozzarella", "Toppings": ["pepperoni", "sausage", "ham", "bacon"], "Price": 15.00},
    "Veggie": {"Sauce": "tomato", "Cheese": "mozzarella", "Toppings": ["bell peppers", "onions", "mushrooms", "olives", "spinach"], "Price": 15.00},
    "BBQ Chicken": {"Sauce": "bbq", "Cheese": "mozzarella", "Toppings": ["grilled chicken", "red onions", "cilantro"], "Price": 15.00},
    "Buffalo Chicken": {"Sauce": "buffalo", "Cheese": "mozzarella", "Toppings": ["spicy chicken", "red onions", "ranch drizzle"], "Price": 15.00},
    "Cheese": {"Sauce": "tomato", "Cheese": "mozzarella", "Toppings": ["cheese"], "Price": 15.00}
}

sauces = ["tomato", "bbq", "buffalo"]
cheeses = ["mozzarella", "mozzarella slices"]
proteins = ["pepperoni", "ham", "sausage", "bacon", "grilled chicken", "spicy chicken"]
veggies = ["fresh basil", "olive oil", "tomatoes", "pineapple", "bell peppers", "onions", "mushrooms", "olives", "spinach", "red onions", "cilantro", "ranch drizzle"]

class PizzaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PizzaPy Ordering Menu")
        self.geometry("700x1000")
        self.configure(bg="#2e2e2e")  # Dark background

        self.cart = []
        self.protein_selected = set()
        self.veggie_selected = set()

        self.create_widgets()

    def create_widgets(self):
        # --- Style for dark mode ---
        self.button_style = {"bg": "#4e4e4e", "fg": "white", "activebackground": "#666666",
                             "activeforeground": "white", "highlightbackground": "#4e4e4e",
                             "highlightthickness": 1, "bd": 0, "relief": "flat"}

        # Customer Name
        name_frame = ttk.Frame(self)
        name_frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(name_frame, text="Customer Name:").pack(side="left", padx=5)
        self.name_entry = ttk.Entry(name_frame)
        self.name_entry.pack(side="left", fill="x", expand=True)

        # Specialty Pizzas
        specialty_frame = ttk.LabelFrame(self, text="Specialty Pizzas")
        specialty_frame.pack(fill="x", padx=10, pady=5)

        self.specialty_listbox = tk.Listbox(specialty_frame, height=10, bg="#4e4e4e", fg="white")
        for pizza, details in specialty_pizzas.items():
            toppings_list = ", ".join(details["Toppings"]) if details["Toppings"] else "No Toppings"
            self.specialty_listbox.insert(tk.END, f"{pizza} (${details['Price']:.2f}) - {toppings_list}")
        self.specialty_listbox.pack(fill="both", expand=True, padx=5, pady=5)

        tk.Button(specialty_frame, text="Add Specialty Pizza", command=self.add_specialty_to_cart, **self.button_style).pack(pady=5)

        # Build Your Own Pizza
        build_frame = ttk.LabelFrame(self, text="Build Your Own Pizza")
        build_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(build_frame, text="Custom Name:").grid(row=0, column=0, padx=5, pady=5)
        self.custom_name_entry = ttk.Entry(build_frame)
        self.custom_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(build_frame, text="Sauce:").grid(row=1, column=0, padx=5, pady=5)
        self.sauce_var = tk.StringVar(value=sauces[0])
        self.sauce_combo = ttk.Combobox(build_frame, textvariable=self.sauce_var, values=sauces)
        self.sauce_combo.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(build_frame, text="Cheese:").grid(row=2, column=0, padx=5, pady=5)
        self.cheese_var = tk.StringVar(value=cheeses[0])
        self.cheese_combo = ttk.Combobox(build_frame, textvariable=self.cheese_var, values=cheeses)
        self.cheese_combo.grid(row=2, column=1, padx=5, pady=5)

        toppings_frame = ttk.Frame(build_frame)
        toppings_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        ttk.Label(toppings_frame, text="Proteins:").grid(row=0, column=0, sticky="w")
        self.protein_listbox = tk.Listbox(toppings_frame, selectmode="multiple", height=6, bg="#4e4e4e", fg="white")
        for item in proteins:
            self.protein_listbox.insert(tk.END, item)
        self.protein_listbox.grid(row=1, column=0, padx=5)

        ttk.Label(toppings_frame, text="Veggies:").grid(row=0, column=1, sticky="w")
        self.veggie_listbox = tk.Listbox(toppings_frame, selectmode="multiple", height=6, bg="#4e4e4e", fg="white")
        for item in veggies:
            self.veggie_listbox.insert(tk.END, item)
        self.veggie_listbox.grid(row=1, column=1, padx=5)

        self.selected_toppings_label = tk.Label(build_frame, text="Selected Toppings:", anchor="w", justify="left", bg="#2e2e2e", fg="white")
        self.selected_toppings_label.grid(row=4, column=0, columnspan=2, pady=5)

        toppings_button_frame = tk.Frame(build_frame, bg="#2e2e2e")
        toppings_button_frame.grid(row=5, column=0, columnspan=2, pady=10)

        tk.Button(toppings_button_frame, text="Add Custom Pizza", command=self.add_custom_to_cart, **self.button_style).grid(row=0, column=0, padx=5)
        tk.Button(toppings_button_frame, text="Clear Toppings", command=self.clear_toppings, **self.button_style).grid(row=0, column=1, padx=5)

        self.protein_listbox.bind("<<ListboxSelect>>", self.update_protein_selection)
        self.veggie_listbox.bind("<<ListboxSelect>>", self.update_veggie_selection)


        # Cart
        cart_frame = ttk.LabelFrame(self, text="Your Order")
        cart_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.cart_listbox = tk.Listbox(cart_frame, bg="#4e4e4e", fg="white")
        self.cart_listbox.pack(fill="both", expand=True, padx=5, pady=5)

        tk.Button(cart_frame, text="Remove Selected Item", command=self.remove_item, **self.button_style).pack(pady=5)

        self.total_label = tk.Label(self, text="Total: $0.00", font=("Arial", 14), bg="#2e2e2e", fg="white")
        self.total_label.pack(pady=5)

        button_frame = tk.Frame(self, bg="#2e2e2e")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Checkout", command=self.checkout, **self.button_style).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Save Order to Database", command=self.save_order, **self.button_style).grid(row=0, column=1, padx=10)

    # --- Core Methods ---

    def update_protein_selection(self, event=None):
        selected_now = {self.protein_listbox.get(i) for i in self.protein_listbox.curselection()}
        self.protein_selected.update(selected_now)
        self.update_selected_toppings_display()

    def update_veggie_selection(self, event=None):
        selected_now = {self.veggie_listbox.get(i) for i in self.veggie_listbox.curselection()}
        self.veggie_selected.update(selected_now)
        self.update_selected_toppings_display()

    def update_selected_toppings_display(self):
        all_selected = sorted(list(self.protein_selected | self.veggie_selected))
        self.selected_toppings_label.config(text="Selected Toppings: " + ", ".join(all_selected))



    def clear_toppings(self):
        self.protein_listbox.selection_clear(0, tk.END)
        self.veggie_listbox.selection_clear(0, tk.END)
        self.protein_selected.clear()
        self.veggie_selected.clear()
        self.selected_toppings_label.config(text="Selected Toppings:")

    def add_specialty_to_cart(self):
        selected = self.specialty_listbox.curselection()
        if selected:
            pizza_name = list(specialty_pizzas.keys())[selected[0]]
            price = specialty_pizzas[pizza_name]['Price']
            self.cart.append((pizza_name, price))
            self.update_cart()

    def add_custom_to_cart(self):
        sauce = self.sauce_var.get()
        cheese = self.cheese_var.get()
        custom_name = self.custom_name_entry.get().strip() or "Custom Pizza"

        all_selected = sorted(list(self.protein_selected | self.veggie_selected))
        description = f"{custom_name} ({sauce} sauce, {cheese} cheese, {', '.join(all_selected)})"
        price = 2.00 + len(all_selected) * 1.00

        self.cart.append((description, price))
        self.update_cart()
        self.clear_toppings()

    def update_cart(self):
        self.cart_listbox.delete(0, tk.END)
        total = 0
        for item, price in self.cart:
            self.cart_listbox.insert(tk.END, f"{item} - ${price:.2f}")
            total += price
        self.total_label.config(text=f"Total: ${total:.2f}")

    def remove_item(self):
        selected = self.cart_listbox.curselection()
        if selected:
            del self.cart[selected[0]]
            self.update_cart()

    def checkout(self):
        if not self.cart:
            messagebox.showwarning("Cart Empty", "Your cart is empty!")
            return
        customer_name = self.name_entry.get().strip()
        if not customer_name:
            messagebox.showwarning("Missing Name", "Please enter a customer name before checkout.")
            return
        order_details = "\n".join([item for item, _ in self.cart])
        total = sum([price for _, price in self.cart])
        messagebox.showinfo("Receipt", f"Customer: {customer_name}\n\nOrder Summary:\n{order_details}\n\nTotal: ${total:.2f}\n\nThank you for your order!")
        self.cart.clear()
        self.update_cart()

    def save_order(self):
        if not self.cart:
            messagebox.showwarning("Cart Empty", "Add items to your cart before saving.")
            return
        customer_name = self.name_entry.get().strip()
        if not customer_name:
            messagebox.showwarning("Missing Name", "Please enter a customer name before saving.")
            return
        description = "; ".join([item for item, _ in self.cart])
        total = sum([price for _, price in self.cart])

        try:
            conn = sqlite3.connect("pizzapy.db")
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS orders (customer_name TEXT, description TEXT, total_price REAL)")
            cursor.execute("INSERT INTO orders (customer_name, description, total_price) VALUES (?, ?, ?)", (customer_name, description, total))
            conn.commit()
            conn.close()
            messagebox.showinfo("Saved", "Order saved to database!")
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save order: {e}")

if __name__ == "__main__":
    app = PizzaApp()
    app.mainloop()

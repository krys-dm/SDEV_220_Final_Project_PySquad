import sqlite3
import tkinter as tk
from tkinter import messagebox

# Connect to the database
conn = sqlite3.connect('UTF-8pizzapy(1).db')
cursor = conn.cursor()

# Get menu items from database
def fetch_menu():
    cursor.execute("SELECT id, name, price FROM menu")
    return cursor.fetchall()

# Main application
class PizzaOrderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pizza-Py Ordering System")

        self.menu_items = fetch_menu()
        self.cart = []

        self.create_widgets()

    def create_widgets(self):
        # Menu label
        menu_label = tk.Label(self.root, text="Menu", font=("Helvetica", 16))
        menu_label.pack(pady=10)

        # Menu list
        self.menu_listbox = tk.Listbox(self.root, width=50)
        for item in self.menu_items:
            self.menu_listbox.insert(tk.END, f"{item[1]} - ${item[2]:.2f}")
        self.menu_listbox.pack(pady=10)

        # Add to cart button
        add_button = tk.Button(self.root, text="Add to Order", command=self.add_to_cart)
        add_button.pack(pady=5)

        # Cart label
        cart_label = tk.Label(self.root, text="Your Order", font=("Helvetica", 16))
        cart_label.pack(pady=10)

        # Cart list
        self.cart_listbox = tk.Listbox(self.root, width=50)
        self.cart_listbox.pack(pady=10)

        # Total label
        self.total_label = tk.Label(self.root, text="Total: $0.00", font=("Helvetica", 14))
        self.total_label.pack(pady=10)

        # Place order button
        order_button = tk.Button(self.root, text="Place Order", command=self.place_order)
        order_button.pack(pady=5)

    def add_to_cart(self):
        selection = self.menu_listbox.curselection()
        if not selection:
            messagebox.showwarning("No selection", "Please select a menu item.")
            return

        index = selection[0]
        item = self.menu_items[index]
        self.cart.append(item)
        self.cart_listbox.insert(tk.END, f"{item[1]} - ${item[2]:.2f}")
        self.update_total()

    def update_total(self):
        total = sum(item[2] for item in self.cart)
        self.total_label.config(text=f"Total: ${total:.2f}")

    def place_order(self):
        if not self.cart:
            messagebox.showinfo("Empty Cart", "No items in your order.")
            return

        messagebox.showinfo("Order Placed", "Thank you for your order!")
        self.cart.clear()
        self.cart_listbox.delete(0, tk.END)
        self.update_total()

# Set up the window
if __name__ == "__main__":
    root = tk.Tk()
    app = PizzaOrderApp(root)
    root.mainloop()

# Close the database connection when the app closes
conn.close()

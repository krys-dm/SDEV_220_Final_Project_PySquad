import tkinter as tk
import requests 
from tkinter import messagebox
# Tkinter


class Customer:
    customer_count = 0

    def __init__(self):
        Customer.customer_count += 1
        self.customer_id = Customer.customer_count


# Define Menu Window


def open_Menu_Window():
    new_window = tk.Toplevel(root)
    new_window.title("Menu")
    label = tk.Label(new_window, text="This is Menu Page")
    label.pack()


# Define Order Window


def open_Order_window():
    new_window = tk.Toplevel(root)
    new_window.title("Order Here")
    customer = Customer()
    customer_label = tk.Label(new_window, text=f"Customer ID: {customer.customer_id}")
    customer_label.pack(pady=10)  # Display Customer ID at the top
    label = tk.Label(new_window, text="This is order Page")
    label.pack()


# Main window
root = tk.Tk()
root.title("Food ordering System")

# label
label = tk.Label(root, text="Hello and welcome to ")

# Create Menu Button
button = tk.Button(root, text="Menu", command=open_Menu_Window)
button.pack(pady=20)

# Create Order Button
button = tk.Button(root, text="Order Here", command=open_Order_window)
button.pack(pady=25)

# Create Cart Button
button = tk.Button(root, text="Cart")
button.pack(pady=30)



def fetch_pizzas():
    try:
        response = requests.get("http://127.0.0.1:8000/pizzas/")
        if response.status_code == 200:
            pizzas = response.json()
            pizza_listbox.delete(0, tk.END)  # Clear old list
            for pizza in pizzas:
                pizza_listbox.insert(tk.END, f"{pizza['name']} - ${pizza['price']}")
        else:
            messagebox.showerror("Error", "Failed to load pizzas from server.")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Connection error:\n{e}")
tk.Label(root, text="Available Pizzas").pack()

pizza_listbox = tk.Listbox(root, width=50)
pizza_listbox.pack(pady=10)

tk.Button(root, text="Load Pizzas", command=fetch_pizzas).pack()

root.mainloop()

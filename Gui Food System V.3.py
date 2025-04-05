import tkinter as tk
import sqlite3
import os

# Create or connect to a database
conn = sqlite3.connect('guest_database.db')
c = conn.cursor()

# Drop the existing table if it exists
c.execute('DROP TABLE IF EXISTS guests')

# Create a table with the correct schema
c.execute('''CREATE TABLE guests (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT,
                first_name TEXT,
                last_name TEXT,
                allergies TEXT
            )''')
conn.commit()

# Initialize cart
cart_items = 0

# Def Customer Class
class Customer:
    customer_count = 0

    def __init__(self):
        Customer.customer_count += 1
        self.customer_id = Customer.customer_count

# Save the last logged-in username to a file
def save_last_logged_in(username):
    with open("last_logged_in.txt", "w") as file:
        file.write(username)

# Load the last logged-in username from the file
def load_last_logged_in():
    if os.path.exists("last_logged_in.txt"):
        with open("last_logged_in.txt", "r") as file:
            return file.read().strip()
    return None

# Define Menu Window
def open_Menu_Window():
    new_window = tk.Toplevel(root)
    new_window.title("Menu")
    label = tk.Label(new_window, text="This is Menu Page")
    label.pack()

# Define Order Window
def open_Order_window(user_info):
    def add_item():
        global cart_items
        cart_items += 1
        cart_label.config(text=f"Items in Cart: {cart_items}")

    def remove_item():
        global cart_items
        if cart_items > 0:
            cart_items -= 1
        cart_label.config(text=f"Items in Cart: {cart_items}")

    def submit_order():
        first_name = user_info[3]
        last_name = user_info[4]
        allergies = user_info[5]
        
        print(f"Order submitted by {first_name} {last_name}. Allergies: {allergies}")
        cart_label.config(text=f"Items in Cart: {cart_items}")

    new_window = tk.Toplevel(root)
    new_window.title("Order Here")
    customer = Customer()
    customer_label = tk.Label(new_window, text=f"Customer ID: {customer.customer_id}")
    customer_label.pack(pady=10)  # Display Customer ID at the top

    tk.Label(new_window, text=f"First Name: {user_info[3]}").pack()
    tk.Label(new_window, text=f"Last Name: {user_info[4]}").pack()
    tk.Label(new_window, text=f"Allergies: {user_info[5]}").pack()

    cart_label = tk.Label(new_window, text=f"Items in Cart: {cart_items}")
    cart_label.pack(pady=10)

    add_button = tk.Button(new_window, text="Add Item", command=add_item)
    add_button.pack(pady=10)

    remove_button = tk.Button(new_window, text="Remove Item", command=remove_item)
    remove_button.pack(pady=10)

    submit_button = tk.Button(new_window, text="Submit", command=submit_order)
    submit_button.pack(pady=10)

    cart_button = tk.Button(new_window, text="Cart", command=lambda: print(f"Items in Cart: {cart_items}"))
    cart_button.pack(pady=10)

# Define Sign-In Window
def open_SignIn_window():
    def sign_in():
        username = entry_username.get()
        password = entry_password.get()
        
        # Check credentials
        c.execute("SELECT * FROM guests WHERE username=? AND password=?", (username, password))
        result = c.fetchone()
        
        if result:
            print(f"Welcome back, {result[3]} {result[4]}!")
            save_last_logged_in(username)
            open_Order_window(result)
        else:
            print("Invalid credentials. Please try again.")

    new_window = tk.Toplevel(root)
    new_window.title("Sign In")
    
    tk.Label(new_window, text="Username").pack()
    entry_username = tk.Entry(new_window)
    entry_username.pack()

    tk.Label(new_window, text="Password").pack()
    entry_password = tk.Entry(new_window, show="*")
    entry_password.pack()

    sign_in_button = tk.Button(new_window, text="Sign In", command=sign_in)
    sign_in_button.pack(pady=10)

# Define Sign-Up Window
def open_SignUp_window():
    def sign_up():
        username = entry_username.get()
        password = entry_password.get()
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        allergies = entry_allergies.get()
        
        # Insert guest details into the database
        try:
            c.execute("INSERT INTO guests (username, password, first_name, last_name, allergies) VALUES (?, ?, ?, ?, ?)",
                      (username, password, first_name, last_name, allergies))
            conn.commit()
            print(f"Account created for {first_name} {last_name}.")
            new_window.destroy()  # Close the sign-up window
        except sqlite3.IntegrityError:
            print("Username already exists. Please choose a different username.")

    new_window = tk.Toplevel(root)
    new_window.title("Sign Up")
    
    tk.Label(new_window, text="Username").pack()
    entry_username = tk.Entry(new_window)
    entry_username.pack()

    tk.Label(new_window, text="Password").pack()
    entry_password = tk.Entry(new_window, show="*")
    entry_password.pack()

    tk.Label(new_window, text="First Name").pack()
    entry_first_name = tk.Entry(new_window)
    entry_first_name.pack()

    tk.Label(new_window, text="Last Name").pack()
    entry_last_name = tk.Entry(new_window)
    entry_last_name.pack()

    tk.Label(new_window, text="Allergies").pack()
    entry_allergies = tk.Entry(new_window)
    entry_allergies.pack()

    sign_up_button = tk.Button(new_window, text="Sign Up", command=sign_up)
    sign_up_button.pack(pady=10)

# Main window 
root = tk.Tk() 
root.title("Food ordering System")

# Label
label = tk.Label(root, text="Hello and welcome to ")
label.pack()

# Create a frame for the buttons
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

# Create Sign-In Button
button_sign_in = tk.Button(frame_buttons, text="Sign In", command=open_SignIn_window)
button_sign_in.grid(row=0, column=0, padx=10)

# Create Sign-Up Button
button_sign_up = tk.Button(frame_buttons, text="Sign Up", command=open_SignUp_window)
button_sign_up.grid(row=0, column=1, padx=10)

# Create Menu Button
button_menu = tk.Button(frame_buttons, text="Menu", command=open_Menu_Window)
button_menu.grid(row=1, column=0, padx=10, pady=10)

# Create Order Button
button_order = tk.Button(frame_buttons, text="Order Here", command=lambda: open_Order_window(None))
button_order.grid(row=1, column=1, padx=10, pady=10)

# Create Cart Button
button_cart = tk.Button(frame_buttons, text="Cart", command=lambda: print(f"Items in Cart: {cart_items}"))
button_cart.grid(row=1, column=2, padx=10, pady=10)

# Load last logged-in user
last_logged_in_username = load_last_logged_in()
if last_logged_in_username:
    c.execute("SELECT * FROM guests WHERE username=?", (last_logged_in_username,))
    user_info = c.fetchone()
    if user_info:
        open_Order_window(user_info)

# Run the application
root.mainloop()

# Close the database connection when the application exits
conn.close()
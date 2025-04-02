import tkinter as tk

#Def Customer Class
class Customer:
    customer_count = 0

    def __init__(self):
        Customer.customer_count +=1
        self.customer_id = Customer.customer_count

#Define Menu Window
def open_Menu_Window():
    new_window = tk.Toplevel(root)
    new_window.title("Menu")
    label = tk.Label(new_window, text="This is Menu Page")
    label.pack()

#Define Order Window
def open_Order_window():
    new_window = tk.Toplevel(root)
    new_window.title("Order Here")
    customer = Customer()
    customer_label = tk.Label(new_window, text=f"Customer ID: {customer.customer_id}")
    customer_label.pack(pady=10)  # Display Customer ID at the top
    label = tk.Label(new_window, text="This is order Page")
    label.pack()

#Main window 
root = tk.Tk() 
root.title("Food ordering System")

#label
label = tk.Label(root, text="Hello and welcome to ")

#Create Menu Button
button = tk.Button(root, text="Menu", command=open_Menu_Window)
button.pack(pady=20)

#Create Order Button
button = tk.Button(root, text="Order Here", command=open_Order_window)
button.pack(pady=25)

#Create Cart Button
button = tk.Button(root, text="Cart")
button.pack(pady=30) 


root.mainloop()
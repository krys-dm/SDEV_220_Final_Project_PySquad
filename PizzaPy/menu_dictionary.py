"""
Mark Klein
4/18/25

Utilizing the layout of Orlando's menu class, I have made a full list of specialty pizzas wit their sauce, cheese, toppings, and price
I set all prices to 15.00 as im unsure how we want to price the food at the moment. i googled top ten specialty pizzas and copied the ingredients and information from
an article. I also changed the def show_menu function to show the name of the pizza as well as all of its details. and added a show_ingredients function that is basically the same thing for ingredients.


I also added a dictionary for the specific ingredients for the custom pizza to be customized. I used all the ingredients that was listed in the specialty pizza's.
Although if we just add the ingredients the pizza is too cheap, so im thinking of adding a default pizza option or maybe some sizes so there is a base layer price for the custom ones.



"""

import sqlite3


class Menu:
    def __init__(self):
        self.predefined_ingredients = {
            "sauces": {"tomato": 1.00, "bbq": 1.00, "buffalo": 1.00},
            "cheeses": {"mozzarella": 1.00, "mozzarella slices": 1.00},
            "toppings": {
                "fresh basil": 1.00,
                "olive oil": 1.00,
                "tomatoes": 1.00,
                "pepperoni": 1.00,
                "ham": 1.00,
                "pineapple": 1.00,
                "sausage": 1.00,
                "bacon": 1.00,
                "bell peppers": 1.00,
                "onions": 1.00,
                "mushrooms": 1.00,
                "olives": 1.00,
                "spinach": 1.00,
                "grilled chicken": 1.00,
                "red onions": 1.00,
                "cilantro": 1.00,
                "spicy chicken": 1.00,
                "ranch drizzle": 1.00,
            },
        }

        self.predefined_pizzas = {
            "margherita": {
                "sauce": "tomato",
                "cheese": "mozzarella slices",
                "toppings": ["fresh basil", "olive oil", "tomatoes"],
                "price": 15.00,
            },
            "pepperoni": {
                "sauce": "tomato",
                "cheese": "mozzarella",
                "toppings": ["pepperoni"],
                "price": 15.00,
            },
            "hawaiian": {
                "sauce": "tomato",
                "cheese": "mozzarella",
                "toppings": ["ham", "pineapple"],
                "price": 15.00,
            },
            "meat_lovers": {
                "sauce": "tomato",
                "cheese": "mozzarella",
                "toppings": ["pepperoni", "sausage", "ham", "bacon"],
                "price": 15.00,
            },
            "veggie": {
                "sauce": "tomato",
                "cheese": "mozzarella",
                "toppings": [
                    "bell peppers",
                    "onions",
                    "mushrooms",
                    "olives",
                    "spinach",
                ],
                "price": 15.00,
            },
            "bbq_chicken": {
                "sauce": "bbq",
                "cheese": "mozzarella",
                "toppings": ["grilled chicken", "red onions", "cilantro"],
                "price": 15.00,
            },
            "buffalo_chicken": {
                "sauce": "buffalo",
                "cheese": "mozzarella",
                "toppings": ["spicy chicken", "red onions", "ranch drizzle"],
                "price": 15.00,
            },
            "cheese": {
                "sauce": "tomato",
                "cheese": "mozzarella",
                "toppings": [],
                "price": 15.00,
            },
        }

    def show_ingredients(self):
        print("Ingredients!\n")
        for category, items in self.predefined_ingredients.items():
            print(f"{category.title()}:")
            for name, price in items.items():
                print(f"  - {name} (${price:.2f})")
            print()

    def show_menu(self):
        print("Specialty Pizzas!\n")
        for name, details in self.predefined_pizzas.items():
            print(f"{name.replace('_', ' ').title()}:")
            print(f"  Sauce: {details['sauce']}")
            print(f"  Cheese: {details['cheese']}")
            print(
                f"  Toppings: {', '.join(details['toppings']) if details['toppings'] else 'None'}"
            )
            print(f"  Price: ${details['price']:.2f}\n")

    def save_to_database(self):
        connection = sqlite3.connect("pizzapy.db")
        cursor = connection.cursor()

        # Create tables if they don't exist
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ingredients (
                name TEXT,
                category TEXT,
                price REAL
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS pizzas (
                name TEXT,
                sauce TEXT,
                cheese TEXT,
                toppings TEXT,
                price REAL
            )
        """
        )

        #Clear tables to avoid repeated inserts
        cursor.execute("DELETE FROM ingredients")
        cursor.execute("DELETE FROM pizzas")
        
        
        # Insert ingredients
        for category, items in self.predefined_ingredients.items():
            for name, price in items.items():
                cursor.execute(
                    """
                    INSERT INTO ingredients (name, category, price)
                    VALUES (?, ?, ?)
                """,
                    (name, category, price),
                )

        # Insert pizzas
        for pizza_name, details in self.predefined_pizzas.items():
            toppings_string = (
                ", ".join(details["toppings"]) if details["toppings"] else ""
            )
            cursor.execute(
                """
                INSERT INTO pizzas (name, sauce, cheese, toppings, price)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    pizza_name,
                    details["sauce"],
                    details["cheese"],
                    toppings_string,
                    details["price"],
                ),
            )

        connection.commit()
        
        #Selects all information and prints from pizza database
        for row in cursor.execute("SELECT * from pizzas"):
            print(row)
        
        print("*****************************************")
            
        #Selects specific data
        cursor.execute("SELECT * from pizzas where name=:C",{"C": "meat_lovers"} )
        pizza_search = cursor.fetchall()
        print(pizza_search)
        
        connection.close()
        


menu = Menu()
menu.show_ingredients()
menu.show_menu()
menu.save_to_database()

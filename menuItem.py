# Orlado Valadez
#  4/7/25 - start
class Menu:
    def __init__(self):
        self.predefined_pizzas = {
            "pepperoni": {"sauce": "tomato", "ingredients": ["pepperoni"]},
            "cheese": {"sauce": "tomato", "ingredients": ["mozzarella"]},
        }

    def show_menu(self):
        print("Available Pizzas:")
        for pizza in self.predefined_pizzas:
            print(f"- {pizza.title()}")

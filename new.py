from neuralintents.assistants import BasicAssistant

# Sample menu items with prices for the assistant (Real-time data would come from a database or API)
menu_items = {
    "Pizza": 12.99,
    "Burger": 8.99,
    "Pasta": 10.99,
    "Salad": 6.99
}

# Keep track of the order and total amount
order_list = []
total_amount = 0

def show_menu():
    print("Here’s our menu:")
    for item, price in menu_items.items():
        print(f"{item}: ${price}")

def take_order():
    global total_amount
    order = input("What would you like to order? ").capitalize()
    if order in menu_items:
        order_list.append(order)
        total_amount += menu_items[order]
        print(f"Great choice! You've ordered {order}.")
    else:
        print(f"Sorry, we don’t have {order} on the menu. Please choose something from the list.")

def print_bill():
    global total_amount
    print(f"Your current order: {', '.join(order_list)}")
    print(f"Total: ${total_amount:.2f}")
    print("Thank you for dining with us!")

def show_specials():
    print("Today's specials: Grilled Salmon, Spaghetti Bolognese, and Garlic Bread.")

def make_recommendation():
    print("I recommend our signature Pizza and Pasta. They are customer favorites!")

def show_ingredients(dish):
    ingredients = {
        "Pizza": "Dough, Cheese, Tomato Sauce, Pepperoni",
        "Pasta": "Penne, Tomato Sauce, Basil, Garlic",
        "Burger": "Beef Patty, Lettuce, Tomato, Cheese, Bun"
    }
    print(f"The ingredients of {dish} are: {ingredients.get(dish, 'Sorry, we don’t have details for this dish.')}.")

# Initialize assistant with custom method mappings
assistant = BasicAssistant('intents.json', method_mappings={
    "order": take_order,
    "menu": show_menu,
    "bill": print_bill,
    "specials": show_specials,
    "recommendation": make_recommendation,
    "ingredients": show_ingredients,
    "goodbye": lambda: exit(0)
})

# Train and save the model
assistant.fit_model(epochs=50)
assistant.save_model()

# Running the assistant
done = False
while not done:
    message = input("Enter a message: ")
    if message == "STOP":
        done = True
    else:
        print(assistant.process_input(message))

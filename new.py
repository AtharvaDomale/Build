import numpy as np
from neuralintents.assistants import BasicAssistant
from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

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

# Enhanced intent file with new responses
intents = {
    "intents": [
        {"tag": "greeting", "patterns": ["Hi", "Hello", "Good evening", "How are you?"], "responses": ["Hello, welcome to the restaurant!", "Good evening, how can I assist you today?"]},
        {"tag": "order", "patterns": ["I'd like to order", "Can I place an order?", "I want to order food", "Order food"], "responses": ["What would you like to order?"]},
        {"tag": "menu", "patterns": ["Show me the menu", "What do you have?", "Tell me about the menu", "What food do you serve?"], "responses": ["Here’s our menu: Pizza, Burger, Pasta, Salad."]},
        {"tag": "bill", "patterns": ["How much is the bill?", "Can I get the bill?", "What’s the total?", "Check, please!"], "responses": ["Sure, let me get the bill for you."]},
        {"tag": "specials", "patterns": ["What are today's specials?", "Any specials today?", "What is on special today?"], "responses": ["Today we have: Grilled Salmon, Spaghetti Bolognese, and Garlic Bread."]},
        {"tag": "recommendation", "patterns": ["What do you recommend?", "What's your best dish?", "Can you recommend something?"], "responses": ["I recommend our signature Pizza and Pasta. They are customer favorites!"]},
        {"tag": "ingredients", "patterns": ["What ingredients are in the Pizza?", "Tell me the ingredients of the Pasta", "What’s in the Burger?"], "responses": ["Pizza: Dough, Cheese, Tomato Sauce, Pepperoni", "Pasta: Penne, Tomato Sauce, Basil, Garlic", "Burger: Beef Patty, Lettuce, Tomato, Cheese, Bun"]},
        {"tag": "goodbye", "patterns": ["Goodbye", "Thank you", "See you later", "Take care"], "responses": ["Thank you for visiting, have a great day!", "Goodbye!"]}
    ]
}

# Initialize the assistant with custom method mappings
assistant = BasicAssistant('intents.json', method_mappings={
    "order": take_order,
    "menu": show_menu,
    "bill": print_bill,
    "specials": show_specials,
    "recommendation": make_recommendation,
    "ingredients": show_ingredients,
    "goodbye": lambda: exit(0)
})

# Tokenizer setup for training
tokenizer = Tokenizer()
texts = [intent["patterns"] for intent in intents["intents"]]
flat_texts = [item for sublist in texts for item in sublist]  # Flatten the list of patterns
tokenizer.fit_on_texts(flat_texts)

# Convert patterns to sequences and pad them for uniform length
sequences = tokenizer.texts_to_sequences(flat_texts)
X = pad_sequences(sequences, padding='post')

# Define the output labels (y), one for each intent tag
y = np.array([i for i, intent in enumerate(intents["intents"]) for _ in intent["patterns"]])

# Reshape input to match the expected input shape (3D for LSTM)
X = np.expand_dims(X, axis=1)  # Shape becomes (samples, 1, 57)

# Define the model architecture
model = Sequential()
model.add(LSTM(128, input_shape=(1, X.shape[2])))  # Adjust for 3D input
model.add(Dense(64, activation='relu'))
model.add(Dense(len(intents["intents"]), activation='softmax'))

# Compile the model
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(X, y, epochs=50, batch_size=5)

# Save the trained model
model.save('assistant_model.h5')

# Running the assistant
done = False
while not done:
    message = input("Enter a message: ")
    if message == "STOP":
        done = True
    else:
        print(assistant.process_input(message))

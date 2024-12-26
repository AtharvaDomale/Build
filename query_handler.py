from datetime import datetime

def handle_query(query):
    query = query.lower()
    if "hello" in query:
        return "Hello! How can I assist you today?"
    elif "order" in query:
        return "Sure, what would you like to order?"
    elif "menu" in query:
        return "Our menu includes a variety of dishes. What would you like to know more about?"
    elif "time" in query:
        now = datetime.now()
        return f"The current time is {now.strftime('%H:%M:%S')}"
    elif "checkout" in query:
        return "The checkout time is 12 PM. Would you like to extend your stay?"
    elif "help" in query:
        return "I can help you with ordering food, checking the menu, providing the current time, and checkout information. How can I assist you?"
    else:
        return "I'm sorry, I didn't understand that. How can I assist you?"

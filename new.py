import sys
import json
import speech_recognition as sr
import pyttsx3 as tts
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Speech recognizer and TTS initialization
recognizer = sr.Recognizer()
speaker = tts.init()
speaker.setProperty('rate', 150)

# Load intents from JSON file
with open("waiter_intents.json", "r") as file:
    data = json.load(file)

# Extract training data
X_train = []
y_train = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        X_train.append(pattern)
        y_train.append(intent["tag"])

# Train the intent classifier
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)

model = LogisticRegression()
model.fit(X_train_tfidf, y_train)

# Sample menu and order list
menu = {
    "pizza": 10.99,
    "pasta": 8.99,
    "burger": 6.99,
    "salad": 5.99,
    "soda": 1.99
}
order = []

# Functions for waiter intents
def respond(tag):
    for intent in data["intents"]:
        if intent["tag"] == tag:
            response = intent["responses"][0]
            speaker.say(response)
            speaker.runAndWait()
            return

def take_order():
    global recognizer

    speaker.say("What would you like to order?")
    speaker.runAndWait()

    try:
        with sr.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            item = recognizer.recognize_google(audio)
            item = item.lower()

            if item in menu:
                order.append(item)
                speaker.say(f"I have added {item} to your order.")
            else:
                speaker.say(f"Sorry, we don't have {item} on the menu.")
            speaker.runAndWait()
    except sr.UnknownValueError:
        recognizer = sr.Recognizer()
        speaker.say("I didn't catch that. Please try again.")
        speaker.runAndWait()

def show_menu():
    speaker.say("Here is the menu:")
    for item, price in menu.items():
        speaker.say(f"{item}: ${price}")
    speaker.runAndWait()

def get_bill():
    if not order:
        speaker.say("You haven't ordered anything yet.")
    else:
        total = sum(menu[item] for item in order)
        speaker.say(f"Your total is ${total:.2f}.")
    speaker.runAndWait()

def exit_system():
    speaker.say("Thank you for visiting! Have a great day!")
    speaker.runAndWait()
    sys.exit(0)

# Map functions to tags
intent_methods = {
    "greeting": lambda: respond("greeting"),
    "take_order": take_order,
    "show_menu": show_menu,
    "recommend_dish": lambda: respond("recommend_dish"),
    "get_bill": get_bill,
    "exit": exit_system
}

# Main loop for waiter assistant
def waiter_assistant():
    global recognizer

    while True:
        try:
            speaker.say("Listening...")
            speaker.runAndWait()

            with sr.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                message = recognizer.recognize_google(audio)
                message = message.lower()

            X_test_tfidf = vectorizer.transform([message])
            intent = model.predict(X_test_tfidf)[0]

            if intent in intent_methods:
                intent_methods[intent]()
            else:
                speaker.say("I didn't understand that. Could you please repeat?")
                speaker.runAndWait()

        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            speaker.say("I didn't catch that. Please try again.")
            speaker.runAndWait()

if __name__ == "__main__":
    waiter_assistant()

import sys
import threading
import tkinter as tk

import speech_recognition as sr
import pyttsx3 as tts
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Speech recognizer and TTS initialization
recognizer = sr.Recognizer()
speaker = tts.init()
speaker.setProperty('rate', 150)

# Define intents and training data
X_train = [
    "hello", "hi", "hey there", "create a note", "make a note",
    "add to my to-do list", "new task", "show my to-do list",
    "list todos", "exit the program", "quit", "bye"
]
y_train = [
    "greeting", "greeting", "greeting", "create_note", "create_note",
    "add_todo", "add_todo", "show_todos", "show_todos",
    "exit", "exit", "exit"
]

# Train the intent classifier
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)

model = LogisticRegression()
model.fit(X_train_tfidf, y_train)

# To-Do List
todo_list = []

# Functions for intents
def create_note():
    global recognizer

    speaker.say("What would you like to write in the note?")
    speaker.runAndWait()

    try:
        with sr.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            note = recognizer.recognize_google(audio)
            note = note.lower()

            speaker.say("What should I name the file?")
            speaker.runAndWait()

            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            filename = recognizer.recognize_google(audio)
            filename = filename.lower()

        with open(f"{filename}.txt", "w") as f:
            f.write(note)
            speaker.say(f"Successfully created the note {filename}.")
            speaker.runAndWait()

    except sr.UnknownValueError:
        recognizer = sr.Recognizer()
        speaker.say("I didn't catch that. Please try again.")
        speaker.runAndWait()

def add_todo():
    global recognizer

    speaker.say("What would you like to add to your to-do list?")
    speaker.runAndWait()

    try:
        with sr.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            item = recognizer.recognize_google(audio)
            item = item.lower()

            todo_list.append(item)
            speaker.say(f"Added {item} to your to-do list.")
            speaker.runAndWait()
    except sr.UnknownValueError:
        recognizer = sr.Recognizer()
        speaker.say("I didn't catch that. Please try again.")
        speaker.runAndWait()

def show_todos():
    if not todo_list:
        speaker.say("Your to-do list is empty.")
    else:
        speaker.say("Here are the items on your to-do list:")
        for item in todo_list:
            speaker.say(item)
    speaker.runAndWait()

def hello():
    speaker.say("Hello! What can I do for you?")
    speaker.runAndWait()

def quit_app():
    speaker.say("Goodbye!")
    speaker.runAndWait()
    sys.exit(0)

# Intent mapping
intent_methods = {
    "greeting": hello,
    "create_note": create_note,
    "add_todo": add_todo,
    "show_todos": show_todos,
    "exit": quit_app
}

# Main loop for voice assistant
def main_loop():
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
                speaker.say("I don't understand that command.")
                speaker.runAndWait()

        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            speaker.say("I didn't catch that. Please try again.")
            speaker.runAndWait()

if __name__ == "__main__":
    main_loop()

# voice_assistant.py

import speech_recognition as sr
import pyttsx3
from datetime import datetime

def recognize_speech(timeout=5):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=30)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            print("Could not request results; check your network connection.")
            return ""
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start.")
            return ""

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def handle_query(query):
    if "hello" in query.lower():
        return "Hello! How can I assist you today?"
    elif "time" in query.lower():
        now = datetime.now()
        return f"The current time is {now.strftime('%H:%M:%S')}"
    else:
        return "I'm sorry, I didn't understand that."

def main():
    speak("Hello! How can I assist you today?")
    while True:
        query = recognize_speech()
        if query:
            response = handle_query(query)
            speak(response)
            if "exit" in query.lower():
                speak("Goodbye!")
                break

if __name__ == "__main__":
    main()

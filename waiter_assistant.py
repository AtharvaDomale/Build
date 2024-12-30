import time
import speech_recognition as sr
import pyttsx3

class WaiterAssistant:
    def __init__(self):
        self.customer_name = ""
        self.customer_order = ""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()

    def speak(self, text):
        """Convert text to speech."""
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def listen(self):
        """Listen to the microphone and return the speech as text."""
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            print("Listening for your command...")
            audio = self.recognizer.listen(source)

        try:
            print("Recognizing...")
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that. Can you repeat please?")
            return None
        except sr.RequestError:
            self.speak("Sorry, there was an error with the speech recognition service.")
            return None

    def greet_customer(self):
        self.speak("Hello! I am your virtual waiter. My name is Reddy. I will assist you with your order today.")
        time.sleep(2)

    def ask_for_name(self):
        self.speak("May I know your name, please?")
        self.customer_name = self.listen()
        if self.customer_name:
            self.speak(f"Hello {self.customer_name}, welcome!")
        else:
            self.speak("I am sorry, I couldn't hear your name. Can you please say it again?")
            self.ask_for_name()

    def take_order(self):
        self.speak(f"What would you like to order today, {self.customer_name}?")
        self.customer_order = self.listen()
        if self.customer_order:
            self.speak(f"Great! You have ordered {self.customer_order}.")
        else:
            self.speak("I didn't catch that. Can you repeat your order?")
            self.take_order()

    def confirm_order(self):
        self.speak(f"Let me confirm your order: {self.customer_order}. Is that correct?")
        confirmation = self.listen()
        if confirmation and "yes" in confirmation.lower():
            self.speak("Your order has been confirmed!")
        else:
            self.speak("Okay, let's try again.")
            self.take_order()

    def save_order(self):
        try:
            with open('orders.txt', 'a') as file:
                file.write(f"Customer: {self.customer_name}, Order: {self.customer_order}\n")
            self.speak(f"Order for {self.customer_name} saved successfully!")
        except Exception as e:
            self.speak(f"Error saving order: {e}")

    def thank_customer(self):
        self.speak("Thank you for your order! Your food will be served shortly.")

    def run(self):
        self.greet_customer()
        self.ask_for_name()
        self.take_order()
        self.confirm_order()
        self.save_order()
        self.thank_customer()

if __name__ == "__main__":
    waiter = WaiterAssistant()
    waiter.run()





import sys 
import threading
import tkinter as tk

import speech_recognition as sr
import pyttsx3 as tts

from neuralintents import GenericAssistant


recognizer = sr.Recognizer()

speaker = tts.init()
speaker.setProperty('rate', 150)


def basic_function():
    global recognizer



    speaker.say("what you need to order")
    speaker.runAndWait()

    done = False

    while not done:
        try :

            with sr.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                note = recognizer.recognize_google(audio)
                note = note.lower()

                print(note)

                speaker.say("you said" + note)
                speaker.runAndWait()



assistant = GenericAssistant('intents.json')
assistant.train_model()



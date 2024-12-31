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

                speaker.say("choose a file  ")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                filname = recognizer.recognize_google(audio)
                filname = filname.lower()
            
            with open(filname, 'w') as f:
                f.write(note)
                done = True
                speaker.say("i sucessfully created the note{filename}")
                speaker.runAndWait()

        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            speaker.say("i did not understand you, please try again")
            speaker.runAndWait()

def add_todo():

    global recognizer

    speaker.say("what do you want to add to your todo list")
    speaker.runAndWait()

    done = False


    while not done:

        try:

            with sr.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                item = recognizer.recognize_google(audio)
                item = item.lower()

                todo_list.append(item)
                done = True

                speaker.say(f"i added {item} to the to do list")
                speaker.runAndWait()
        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            speaker.say("i did not understand you, please try again")
            speaker.runAndWait()





def show_todos():

    speaker.say("the items on your to do list are the following")
    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()



def hello():
    speaker.say("hello what can i do for you")
    speaker.runAndWait()


def quit():
    speaker.say("bye")
    speaker.runAndWait()
    sys.exit(0)



mappings = {
    "greeting": hello,
    "create_note": basic_function,
    "add_todo": add_todo,
    "show_todos": show_todos,
    "exit": quit
}


assistant = GenericAssistant('intents.json')
assistant.train_model()

while True:

    try:

        with sr.Microphone() as mic:

            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            message = recognizer.recognize_google(audio)
            message = message.lower()

        assistant.request(message)

    except sr.UnknownValueError:
        recognizer = sr.Recognizer()

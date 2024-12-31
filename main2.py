import sys 
import threading
import tkinter as tk

import speech_recognition as sr
import pyttsx3 as tts

from neuralintents import GenericAssistant


recognizer = sr.Recognizer()

speaker = tts.init()
speaker.setProperty('rate', 150)


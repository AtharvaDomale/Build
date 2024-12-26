from speech_rec import recognize_speech
from text_to_speech import speak
from query_handler import handle_query

def main():
    speak("Hello! How can I assist you today?")
    while True:
        query = recognize_speech()
        if query:
            response = handle_query(query)
            speak(response)
            if "exit" in query:
                speak("Goodbye! Have a great day!")
                break

if __name__ == "__main__":
    main()

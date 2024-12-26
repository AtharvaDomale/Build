from speech_rec import recognize_speech
from text_to_speech import speak
from query_handler import handle_query

def main():
    speak("Hello! How can I assist you today?")
    while True:
        query = recognize_speech()
        if query:
            speak(f"You said: {query}")
            response = handle_query(query)
            speak(response)
            speak("Do you need any other help?")
            additional_query = recognize_speech()
            if additional_query:
                speak(f"You said: {additional_query}")
                additional_response = handle_query(additional_query)
                speak(additional_response)
            if "exit" in query.lower() or "exit" in additional_query.lower():
                speak("Goodbye! Have a great day!")
                break

if __name__ == "__main__":
    main()

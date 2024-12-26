import speech_recognition as sr
import time

def recognize_speech(timeout=5, phrase_time_limit=10, silence_threshold=2):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

        # Detect silence to determine if the user has finished speaking
        last_audio_time = time.time()
        while (time.time() - last_audio_time) < silence_threshold:
            try:
                new_audio = recognizer.listen(source, timeout=1, phrase_time_limit=1)
                audio = sr.AudioData(audio.get_raw_data() + new_audio.get_raw_data(),
                                     audio.sample_rate, audio.sample_width)
                last_audio_time = time.time()
            except sr.WaitTimeoutError:
                pass

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

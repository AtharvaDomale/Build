import os
import wave
import json
from vosk import Model, KaldiRecognizer
import pyaudio

class OfflineSpeechToText:
    def __init__(self, model_path="vosk-model-small-en-us-0.15"):
        # Initialize with the model path
        self.model_path = model_path
        self.model = None
        self.recognizer = None

        # Load the model
        self.load_model()

    def load_model(self):
        """Load the Vosk model."""
        if not os.path.exists(self.model_path):
            print(f"Model path does not exist: {self.model_path}")
            return
        print("Loading Vosk model...")
        self.model = Model(self.model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)

    def record_audio(self, duration=5):
        """Record audio using PyAudio and return the audio data."""
        p = pyaudio.PyAudio()

        # Set audio parameters
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=4000)

        print("Recording...")

        frames = []
        for _ in range(0, int(16000 / 1024 * duration)):
            data = stream.read(1024)
            frames.append(data)

        print("Recording stopped.")
        stream.stop_stream()
        stream.close()
        p.terminate()

        return b"".join(frames)

    def transcribe_audio(self, audio_data):
        """Transcribe audio data to text."""
        if not self.recognizer.AcceptWaveform(audio_data):
            return None
        result = self.recognizer.Result()
        return json.loads(result).get("text")

    def save_audio_to_file(self, audio_data, filename="output.wav"):
        """Save the audio data to a WAV file."""
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(audio_data)

    def transcribe_from_microphone(self, duration=5):
        """Record audio from the microphone and transcribe it."""
        audio_data = self.record_audio(duration)
        self.save_audio_to_file(audio_data)

        # Perform transcription
        text = self.transcribe_audio(audio_data)
        if text:
            print("Transcription: ", text)
        else:
            print("No speech detected in the recording.")

if __name__ == "__main__":
    # Initialize the offline speech-to-text system
    stt = OfflineSpeechToText()

    # Record and transcribe audio for 5 seconds
    stt.transcribe_from_microphone(duration=5)

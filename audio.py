import deepspeech
import wave
import numpy as np

# Path to the pre-trained model and scorer (if you downloaded it)
model_path = 'path_to_your_model/deepspeech-0.9.3-models.pbmm'
scorer_path = 'path_to_your_model/deepspeech-0.9.3-models.scorer'  # Optional but recommended

# Load the DeepSpeech model
model = deepspeech.Model(model_path)

# Load the scorer (optional but recommended for better accuracy)
model.enableExternalScorer(scorer_path)

# Path to your audio file
audio_file_path = 'path_to_your_audio_file/audio_file.wav'

# Read the audio file
with wave.open(audio_file_path, 'rb') as wf:
    frames = wf.readframes(wf.getnframes())
    audio_data = np.frombuffer(frames, dtype=np.int16)

# Perform speech-to-text
text = model.stt(audio_data)

# Output the transcription
print("Transcription: ", text)

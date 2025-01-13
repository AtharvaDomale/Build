import pyaudio
import wave
from webrtcvad import Vad

def record_audio_on_voice_offline(sample_rate=16000, channels=1, chunk=1024, aggressiveness=3, silence_duration=2):
    # Initialize WebRTC VAD
    vad = Vad(aggressiveness)
    
    # Initialize PyAudio
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk)
    
    print("Listening for speech...")
    
    frames = []
    silence_frames = 0
    recording_started = False
    
    while True:
        # Read audio chunk from the stream
        data = stream.read(chunk, exception_on_overflow=False)
        
        # Check if the chunk has speech
        is_speech = vad.is_speech(data, sample_rate)
        
        if is_speech:
            frames.append(data)
            silence_frames = 0
            if not recording_started:
                print("Speech detected, recording...")
                recording_started = True
        elif recording_started:
            silence_frames += 1
            # Stop recording if silence lasts for the specified duration
            if silence_frames > (silence_duration * sample_rate / chunk):
                print("Silence detected, stopping recording.")
                break
    
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    # Save the audio to a BytesIO object
    audio_buffer = BytesIO()
    with wave.open(audio_buffer, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))
    
    print("Recording completed.")
    return audio_buffer.getvalue()

# Record audio when speech starts and stops on silence
recorded_audio = record_audio_on_voice_offline()

# Example: Save the recorded audio to a file
with open("offline_voice_triggered_audio.wav", "wb") as f:
    f.write(recorded_audio)

print("Audio saved to offline_voice_triggered_audio.wav.")

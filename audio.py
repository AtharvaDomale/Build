import pyaudio
import wave
from webrtcvad import Vad
from io import BytesIO


def record_audio_on_voice_offline(sample_rate=16000, channels=1, frame_duration_ms=20, aggressiveness=3, silence_duration=2):
    # Initialize WebRTC VAD
    vad = Vad(aggressiveness)

    # Calculate frame size (bytes) based on sample rate and frame duration
    frame_size = int(sample_rate * (frame_duration_ms / 1000.0) * 2)  # 16-bit PCM (2 bytes per sample)
    valid_frame_sizes = [160, 320, 480, 640, 960, 1440]
    
    if frame_size not in valid_frame_sizes:
        raise ValueError(f"Invalid frame size: {frame_size}. Must be 10ms, 20ms, or 30ms.")

    # Initialize PyAudio
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=frame_size)

    print("Listening for speech...")

    frames = []
    silence_frames = 0
    recording_started = False

    while True:
        # Read audio frame
        try:
            data = stream.read(frame_size, exception_on_overflow=False)
        except Exception as e:
            print(f"Error reading audio frame: {e}")
            continue

        # Validate the data length
        if len(data) != frame_size:
            print(f"Invalid frame length: {len(data)}, expected: {frame_size}")
            continue

        # Check if the frame contains speech
        try:
            is_speech = vad.is_speech(data, sample_rate)
        except Exception as e:
            print(f"Error processing frame: {e}")
            continue

        if is_speech:
            frames.append(data)
            silence_frames = 0
            if not recording_started:
                print("Speech detected, recording...")
                recording_started = True
        elif recording_started:
            silence_frames += 1
            # Stop recording if silence lasts for the specified duration
            if silence_frames > (silence_duration * 1000 / frame_duration_ms):
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

# Save the recorded audio to a file
with open("offline_voice_triggered_audio.wav", "wb") as f:
    f.write(recorded_audio)

print("Audio saved to offline_voice_triggered_audio.wav.")

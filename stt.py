import openai
import sounddevice as sd
import soundfile as sf
import keyboard

# Replace with your OpenAI API key
api_key = "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"
openai.api_key = api_key

def transcribe_audio(audio_path):
    try:
        with open(audio_path, 'rb') as audio_file:
            response = openai.Audio.transcribe("whisper-1", audio_file)
            return response['text']
    except Exception as e:
        print(f"Transcription error: {e}")
        return None

def main():
    # print("Press 'w' to start capturing audio...")

    try:
        # Wait for the 'w' key to be pressed
        keyboard.wait('w')

        # Capture audio from the microphone
        duration = 10  # Recording duration in seconds
        sample_rate = 16000
        audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        sd.wait()

        # Save the captured audio as a WAV file
        audio_path = 'captured_audio.wav'
        sf.write(audio_path, audio_data, sample_rate)

        # Transcribe the saved audio
        text = transcribe_audio(audio_path)
        if text:
            print("Transcribed Text:")
            print(text)
            return text
    except KeyboardInterrupt:
        print("\nRecording stopped.")


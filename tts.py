
from elevenlabs import generate, play
from elevenlabs import set_api_key
set_api_key("d0b12541a0eb5afb8666089aaf1dc309")
global audio
def genAudio(voice,text):
    audio = generate(
        text = text,
        voice = voice,
        model = "eleven_multilingual_v1"    # Low-latencey model specifically trained for English speech
    )

def playAudio():
    play (
        audio,              # This is the audio that was generated above
        notebook=False,     # If True, plays audio in notebook (using IPython.display.Audio)else uses ffmpeg
        use_ffmpeg=False,   # If False, uses sounddevice and soundfile to play audio
    )
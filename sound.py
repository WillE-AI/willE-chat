import pyttsx3

def text_to_speech(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
    
    # Set the rate of speech
    engine.setProperty('rate', 150)  # Speed of speech

    # Set the volume level
    engine.setProperty('volume', 1.0)  # Volume level between 0.0 and 1.0

    # Now say something (this method adds the text to the command queue)
    engine.say(text)
    
    # Play the speech
    engine.runAndWait()

# Example usage
text = input("Enter the text you want to convert to speech: ")
text_to_speech(text)

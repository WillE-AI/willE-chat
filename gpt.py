import os
import openai
import pyttsx3
import pygame
from playsound import playsound
from concurrent.futures import ThreadPoolExecutor
openai.api_key = "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"
# Define the preprompt that sets the context for the AI
preprompt = {"role": "system", "content": "You are a mascot called Willie the wildcat from K-state I want you to act like him and be knowledgeable about K-state. your personality is cheery, unformal, upbeat, you are not an AI language model, you are also sassy. Make your responses SHORT around 16 tokens"}

# Initialize conversation history with the preprompt
conversation_history = [preprompt]


def play_mp3(filename):
    # Initialize pygame mixer
    pygame.mixer.init()
    
    # Construct the relative path to the MP3 file
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = filename
    abs_file_path = os.path.join(script_dir, rel_path)
    
    # Load the MP3 music file
    pygame.mixer.music.load(abs_file_path)
    
    # Start playing the music
    pygame.mixer.music.play()
    
    # Wait for the music to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
   # print(f"Playing {abs_file_path} completed.")



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

def chat_with_openai(user_input):
    global conversation_history  # Use the global conversation history variable
    
    # Add the user's message to the conversation history
    conversation_history.append({"role": "user", "content": user_input})
    
    # Make a call to the OpenAI API with the conversation history
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_history,
        temperature=0.7,
        max_tokens=64,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
   
    # Extract the AI's response and print it
    print(conversation_history)
    ai_message = response['choices'][0]['message']['content']
   # print("AI:", ai_message)
    
   # text_to_speech(ai_message)
    
    
    # Add the AI's response to the conversation history
    conversation_history.append({"role": "system", "content": ai_message})
    
    # Calculate the total length of the conversation without the preprompt
    conversation_length = sum(len(m["content"]) for m in conversation_history[1:])  # Skip the preprompt in the calculation
    
    # If the conversation (excluding the preprompt) exceeds 500 characters, remove the oldest messages after the preprompt
    while conversation_length > 2000:
        # Remove the oldest message after the preprompt
        removed_message = conversation_history.pop(1)  # Remove the second element, index 1
        # Subtract the length of the removed message from the total
        conversation_length -= len(removed_message["content"])
        print("Removed message to maintain length. New length (characters):", conversation_length)
    return ai_message
    
    
def start_genAudio(voice, text):
    audio_thread = threading.Thread(target=genAudio, args=(voice, text))
    audio_thread.start()

# Example conversation loop
def chat(text):
    
    
    return chat_with_openai(text)
    

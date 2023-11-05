import tkinter as tk
from PIL import Image, ImageTk, ImageOps
from pynput import mouse
import threading
import gpt
import keyboard
import sheet
from time import sleep
from collections import deque
from concurrent.futures import ThreadPoolExecutor

faceindex = 3
bodyindex = 1
is_willie_talking = False
is_walking = False
def on_click(x, y, button, pressed):
    if pressed:
        # Use a future to submit the job and add a callback
       
        
        root.after(0, lambda: set_target(x, y))
def ai_submit(text):
    
    if text:  # Check if chat is not empty
        # Create a label with the chat and display it on top
        label = tk.Label(chat_frame, text="Willie: " + text, anchor='w', wraplength=300, fg="white", background='#710193', font=("Arial", 8)) 
        label.pack(side='top', anchor='nw', pady=(5, 0))
        
        # Add the label to our tracking deque
        chat_labels.append(label)
        toggle_animation()
        # If we have too many labels, remove the first one
        if len(chat_labels) > max_labels:
            # Remove the oldest label from the frame and deque
            oldest_label = chat_labels.popleft()
            oldest_label.destroy()

        # Clear the text box for new input
        text_box.delete(0, tk.END)
# Handle the result of the chat function
def handle_result(future):
    try:
        result = future.result()
        print(result)
        ai_submit(result)
        # Update the UI or do something with the result here.
        # Make sure to do this in the main thread.
    except Exception as e:
        # Handle exceptions
        print(f"Error retrieving the result: {e}")

# It's better to create the executor outside of the on_click event
executor = ThreadPoolExecutor(max_workers=1)

  # Function to stop the program when 'q' is pressed
def stop_program(event):
    executor.shutdown(wait=False)
    root.destroy()
def stop_all_threads():
    print("Stopping all threads and exiting...")
    # Shutdown the ThreadPoolExecutor
    executor.shutdown(wait=False)
    
    # Stop the mouse listener
    if listener.running:
        listener.stop()
    
    # Destroy the root Tkinter window to stop the program
    root.destroy()

# Listen for the 'q' key press and stop all threads when detected
keyboard.add_hotkey('`', stop_all_threads)



def clean_alpha(image, threshold=200):
    """ Set all pixels with an alpha value below the threshold to fully transparent. """
    datas = image.getdata()
    newData = []
    for item in datas:
        if item[3] < threshold:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    image.putdata(newData)
    return image


def create_combined_image(face_path, body_path, face_position, faceindex ,bodyindex):
    
    face_img = sheet.extract_single_frame("face_sheet.png",faceindex,534,534,128,128)
    face_image = clean_alpha(face_img)
    
    
    body_img = sheet.extract_single_frame("body_sheet.png",bodyindex,534,534,128,128)
    body_image = clean_alpha(body_img)
    # Create a new empty image with the same size as the body image to composite on
    composite_image = Image.new("RGBA", body_img.size)

    # Paste the body onto the composite image
    composite_image.paste(body_img, (0, 0))

    # Paste the face image onto the composite image at the desired position
    composite_image.paste(face_image, face_position, face_image)

    return composite_image
    
    
    
    
face_image_path = "face_sheet.png"
body_image_path = "body_sheet.png"

face_position = (0, 10)  # Adjust this as necessary

combined_image = create_combined_image(face_image_path, body_image_path, face_position,faceindex,bodyindex)

    
def update_face(frame_delay):
    global faceindex, bodyindex, label, photo, is_willie_talking

    # Only update the sprite if the animation is running
    if is_willie_talking:
        # Increment the sprite index
        
        if is_willie_talking:
            if faceindex == 3:
                faceindex = 4
            else:
                faceindex = 3# loop back to 0 when you reach sprite_count
        print(faceindex)
        # Create a new combined image with the new sprite index
        combined_image = create_combined_image(face_image_path, body_image_path, face_position, faceindex,bodyindex)

        # Convert the image for Tkinter
        photo = ImageTk.PhotoImage(combined_image)

        # Update the label with the new image
        label.configure(image=photo)
        label.image = photo  # keep a reference!

        # Call this function again after a certain delay
        root.after(frame_delay, update_face, frame_delay)
    
    
def update_body(frame_delay):
    global bodyindex, label, photo, is_walking

    # Only update the sprite if the animation is running
    if is_walking:
        # Increment the sprite index
        
        if is_walking:
            if bodyindex == 1:
                bodyindex = 2
            else:
                bodyindex = 1# loop back to 0 when you reach sprite_count
        print(bodyindex)
        # Create a new combined image with the new sprite index
        combined_image = create_combined_image(face_image_path, body_image_path, face_position, faceindex ,bodyindex)

        # Convert the image for Tkinter
        photo = ImageTk.PhotoImage(combined_image)

        # Update the label with the new image
        label.configure(image=photo)
        label.image = photo  # keep a references

        # Call this function again after a certain delay
        root.after(frame_delay, update_body, frame_delay)
        
    
def toggle_animation():
    global is_willie_talking

    # Toggle the state of the animation
    is_willie_talking = not is_willie_talking

    # If the animation is now running, update the sprite immediately
    if is_willie_talking:
        update_face(200)
        # Start a timer to stop talking after 5 seconds (5000 milliseconds)
        root.after(5000, stop_talking)

def stop_talking():
    global is_willie_talking
    if is_willie_talking:
        is_willie_talking = False
        # Optionally update the face to a non-talking sprite

def toggle_walking_animation():
    global is_walking
    
    is_walking = not is_walking
    
    if is_walking:
        update_body(200)

# Start the mouse listener in a separate thread
listener = mouse.Listener(on_click=on_click)
listener.start()
# Listen to mouse clicks

# Create a window
root = tk.Tk()
speech_bubble_image = Image.open("speechbubble.png")
speech_bubble_image = ImageOps.expand(speech_bubble_image, border=20, fill='white')
speech_bubble_photo = ImageTk.PhotoImage(speech_bubble_image)

# Create a Canvas and add the speech bubble image to it
canvas = tk.Canvas(root, width=speech_bubble_image.width, height=speech_bubble_image.height, highlightthickness=0)
#canvas.config(bg='')
#canvas.pack()

canvas.create_image(0, 0, anchor="nw", image=speech_bubble_photo)

# Add a text object to the Canvas
text_id = canvas.create_text(
    speech_bubble_image.width // 2, speech_bubble_image.height // 2,
    text="Your Text Here", font=('Helvetica', 16), fill='black'
)

# Remove the window decorations
root.overrideredirect(True)

# Make the window stay on top
root.wm_attributes("-topmost", True)

# Load an image using PIL
photo = ImageTk.PhotoImage(combined_image)
# Create a label to display the image
label = tk.Label(root, image=photo, bg='white')

# This makes the background transparent
label.master.wm_attributes('-transparentcolor', 'white')

# Lay out the label
label.pack(side=tk.TOP, anchor="e")

# Create a label with some text and make its background match the window
transparent_image_path = 'temp.gif'
trans_image = Image.open(transparent_image_path)
photo1 = ImageTk.PhotoImage(trans_image)

# Create a label with that image
#label = tk.Label(root, text="Hello, Tkinfiasejfseaiojfaoisejfoisaejfoiejsaoifter!", font=("Helvetica", 16), compound='center')

# Add the label to the window
#label.pack()


new_window = tk.Toplevel(root)
new_window.title("Will-E")
new_window.iconbitmap('faces/willE_icon.ico')  # Replace 'path_to_your_icon.ico' with the actual path to your icon file    
new_window.geometry("300x300")  # width x height
new_window.config(background="#222222")

# Container frame for chat labels
chat_frame = tk.Frame(new_window)
chat_frame.pack(fill='both', expand=True)
chat_frame.config(background = '#222222')

# Container frame for input and submit button
input_frame = tk.Frame(new_window, background="#222222")
input_frame.pack(side='bottom')
# Text box for input inside the input frame
text_box = tk.Entry(input_frame, width=25)
text_box.pack(side='left', pady=(5,5), padx=(5,5))
text_box.config(relief=tk.FLAT, borderwidth=0, highlightthickness=0)

# Keep track of the chat labels
chat_labels = deque()
max_labels = 6  # Set the maximum number of labels

# Function to call when the button is clicked
def on_submit():
    # Get the chat from the text box
    chat = text_box.get()
    
    if chat:  # Check if chat is not empty
        # Create a label with the chat and display it on top
        label = tk.Label(chat_frame, text="You: "+chat, anchor='w', wraplength=300, fg="white", background='#222222', font=("Calibri", 8))
        label.pack(side='top', anchor='nw', pady=(5, 0))

        # Add the label to our tracking deque
        chat_labels.append(label)

        # If we have too many labels, remove the first one
        if len(chat_labels) > max_labels:
            # Remove the oldest label from the frame and deque
            oldest_label = chat_labels.popleft()
            oldest_label.destroy()

        # Clear the text box for new input
        text_box.delete(0, tk.END)
        
        start_chat(chat)


# Button to submit the chat inside the input frame
submit_button = tk.Button(input_frame, text=">", command=on_submit, fg="#ffffff", background='#710193', relief=tk.FLAT, borderwidth=0, highlightthickness=0, font=("Calibri", 8), width=3)
submit_button.pack(side='right')
# Button to open the new window
def enter_pressed(event):
    # Function to trigger the button when Enter key is pressed
    submit_button.invoke()
    
root.bind('<Return>', enter_pressed)
text_box.bind('<Return>', enter_pressed)



# If we have too many labels, remove the first one

def update_speech_bubble_text(text):
    canvas.itemconfigure(text_id, text=text)
# Initial position
x = 0
y = 0

# Speed/direction of movement
speed = 10

# Target position (None initially)
target_x, target_y = None, None

# Function to move the window towards the target location
def move_towards_target():
    global x, y, target_x, target_y
    
    if target_x is not None and target_y is not None:
        # Calculate distance from target
        delta_x = target_x - x
        delta_y = target_y - y
        distance = (delta_x**2 + delta_y**2)**0.5

        # Move towards the target if we're not already there
        if distance > speed:
            x += delta_x / distance * speed
            y += delta_y / distance * speed
        else:
            x, y = target_x, target_y
            target_x, target_y = None, None  # Clear the target once we reach it
            toggle_walking_animation()
            bodyindex = 0
            combined_image = create_combined_image(face_image_path, body_image_path, face_position,faceindex,bodyindex)
            photo = ImageTk.PhotoImage(combined_image)

        # Update the label with the new image
            label.configure(image=photo)
            label.image = photo  # keep a reference!
            

    # Move the window to the new position
    root.geometry(f'+{int(x)}+{int(y)}')

    # Schedule the next movement
    root.after(10, move_towards_target)  # Adjust the timing here for faster or slower movement

# Function to set the target position on mouse click
# Function to set the target position directly
def set_target(x, y):
    global target_x, target_y
    toggle_walking_animation()
    target_x = x - combined_image.width // 2
    target_y = y - combined_image.height // 2

def start_chat(text):
    future = executor.submit(gpt.chat, text)
    future.add_done_callback(lambda f: root.after(0, handle_result, f))

# Call start_chat after 0 milliseconds to start the process automatically
#root.after(0, start_chat)

# Function to stop the program when 'q' is pressed
def stop_all_threads():  # Add 'event=None' to allow the function to be called by a key binding
    # Shutdown the ThreadPoolExecutor
    executor.shutdown(wait=False)
    
    # Stop the mouse listener
    listener.stop()
    
    # Destroy the root Tkinter window to stop the program
    root.destroy()


# Start the moving towards target after a short delay
root.after(100, move_towards_target)

# Run the main loop
root.mainloop()

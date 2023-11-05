from PIL import Image

def extract_single_frame(sprite_sheet_path, frame_index, frame_width, frame_height, desired_width, desired_height):
    # Open the sprite sheet image
    sprite_sheet = Image.open(sprite_sheet_path)
    
    # Define the bounding box of the frame
    left = frame_index * frame_width
    upper = 0
    right = left + frame_width
    lower = frame_height
    
    # Crop the sprite sheet to extract the frame
    frame = sprite_sheet.crop((left, upper, right, lower))
    
    # Resize the frame
    resized_frame = frame.resize((desired_width, desired_height), Image.Resampling.LANCZOS)  # or just resize((desired_width, desired_height)) for default resampling
    
    return resized_frame

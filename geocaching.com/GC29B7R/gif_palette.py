from PIL import Image
import random
import os

# chatgpt

def shuffle_palette(gif_path, output_folder, num_variations=5):
    # Open the GIF image
    img = Image.open(gif_path)
    
    # Ensure it's in P mode (palette-based)
    if img.mode != 'P':
        raise ValueError("Image must be in palette (P) mode.")
    
    # Get the original palette
    palette = img.getpalette()
    
    # Split into RGB triplets
    colors = [palette[i:i+3] for i in range(0, len(palette), 3)]
    
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    for i in range(num_variations):
        shuffled_colors = colors[:]
        random.shuffle(shuffled_colors)
        
        # Flatten back into a single list
        new_palette = sum(shuffled_colors, [])
        
        # Create a new image with the shuffled palette
        new_img = img.copy()
        new_img.putpalette(new_palette)
        
        # Save as PNG
        output_path = os.path.join(output_folder, f'shuffled_{i+1}.png')
        new_img.save(output_path, format='PNG')
        print(f"Saved: {output_path}")

# Example usage
gif_path = 'tunel.gif'  # Change this to your actual GIF path
output_folder = 'target'
shuffle_palette(gif_path, output_folder)

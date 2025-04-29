#!/usr/bin/env python3
from PIL import Image
from rembg import remove

# Load the JPEG image
image = Image.open("input_image.jpeg")

out = remove(image)
# Save it as PNG
out.save("output_image.png", "PNG")

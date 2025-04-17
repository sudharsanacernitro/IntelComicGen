from PIL import Image, ImageDraw, ImageFont

def title(heading):
    # Image dimensions
    width, height = 800, 600  # Customize your image size

    # Create a white image
    image = Image.new('RGB', (width, height), color='white')
    
    # Initialize drawing context
    draw = ImageDraw.Draw(image)

    # Text to display
    text = heading

    # Load a font (try different fonts if needed)
    try:
        font = ImageFont.truetype("arial.ttf", size=40)  # Try common system fonts
    except:
        font = ImageFont.load_default()  # Fallback to default font
        print("Using default font - install arial.ttf for better results")

    # NEW: Calculate text size using textbbox (modern Pillow)
    # Get the bounding box of the text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]  # right - left
    text_height = bbox[3] - bbox[1]  # bottom - top

    # Calculate position
    x = (width - text_width) / 2
    y = (height - text_height) / 2

    # Draw the text (black by default)
    draw.text((x, y), text, font=font, fill='black')

    # Save the image
    image.save("./output/A_HEAD.png")
    print("Title-Card Created './output/A_HEAD.png'")

    # # Optional: Show the image
    # image.show()
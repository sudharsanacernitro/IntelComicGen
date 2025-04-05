from PIL import Image, ImageDraw, ImageFont

# Load images
img1 = Image.open("scene1.png").resize((1024, 512))
img2 = Image.open("scene2.png").resize((1024, 512))
img3 = Image.open("scene3.png").resize((512, 1024))

# Load font
font_size = 20
try:
    font = ImageFont.truetype("arial.ttf", font_size)
except:
    font = ImageFont.load_default()

# Wrap text to fit within image width
def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    line = ""

    for word in words:
        test_line = line + word + " "
        if draw.textlength(test_line, font=font) <= max_width:
            line = test_line
        else:
            lines.append(line.strip())
            line = word + " "
    lines.append(line.strip())
    return lines

# Helper to calculate text block height
def get_text_block_height(lines, font):
    line_height = font.getbbox("A")[3]
    return len(lines) * (line_height + 5)

# Spacing
padding = 15
text_height_estimate = font_size * 3
canvas_width = 1024 + 512 + 3 * padding
canvas_height = max(2 * (512 + text_height_estimate) + 3 * padding, 1024 + text_height_estimate + 2 * padding)

# Create canvas
canvas = Image.new("RGB", (canvas_width, canvas_height), "white")
draw = ImageDraw.Draw(canvas)

# Paste image and draw wrapped text below inside the same bounding box
def paste_with_wrapped_text(img, pos, text):
    x, y = pos
    max_text_width = img.width
    lines = wrap_text(text, font, max_text_width, draw)
    text_block_height = get_text_block_height(lines, font)

    # Draw bounding box that includes both image and text
    box_width = img.width
    box_height = img.height + text_block_height + 10
    draw.rectangle([x, y, x + box_width, y + box_height], outline="black", width=5)

    # Paste image inside box
    canvas.paste(img, (x, y))

    # Draw text under image inside box
    text_y = y + img.height + 5
    for line in lines:
        text_width = draw.textlength(line, font=font)
        text_x = x + (img.width - text_width) // 2
        draw.text((text_x, text_y), line, fill="red", font=font)
        text_y += font.getbbox("A")[3] + 5

# Add images with wrapped captions and bounding box
paste_with_wrapped_text(img1, (padding, padding), "Scene 1: A person sitting at a desk filled with paperwork, looking serious in a narrow alleyway.")
paste_with_wrapped_text(img2, (padding, 2 * padding + 512 + text_height_estimate), "Scene 2: The same location as above, but showing a different emotion or mood, symbolizing contrast. hai hello")
paste_with_wrapped_text(img3, (2 * padding + 1024, padding), "Scene 3: The individual is deep in thought, surrounded by scattered papers, representing internal conflict.")

# Save and show
canvas.save("output_wrapped_box_text.png")
canvas.show()

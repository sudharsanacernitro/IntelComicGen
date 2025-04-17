from PIL import Image, ImageDraw, ImageFont
import os

# Configuration
COMIC_IMAGES_DIR = "./comic_images/"  # Folder containing your scene images
OUTPUT_PREFIX = "comic_page_"
HORIZONTAL_SIZE = (1024, 512)  # Size for horizontal images
VERTICAL_SIZE = (512, 1024)    # Size for vertical images
PADDING = 15
FONT_SIZE = 20
TEXT_COLOR = "red"
BORDER_COLOR = "black"
BORDER_WIDTH = 5
BACKGROUND_COLOR = "white"

# Load font
try:
    font = ImageFont.truetype("arial.ttf", FONT_SIZE)
except:
    font = ImageFont.load_default()

def wrap_text(text, font, max_width):
    """Wrap text to fit within specified width"""
    dummy_draw = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        if dummy_draw.textlength(test_line, font=font) <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
        
    return lines

def create_comic_page(scene_paths, scene_texts, output_path):
    """Create a comic page with horizontal images stacked vertically on left and vertical image on right"""
    # Load and resize images
    images = []
    for i, path in enumerate(scene_paths):
        if path and os.path.exists(path):
            img = Image.open(path)
            # Third image in group of 3 is vertical, others horizontal
            size = VERTICAL_SIZE if (len(scene_paths) == 3 and i == 2) else HORIZONTAL_SIZE
            images.append(img.resize(size))
        else:
            print(f"Warning: Image not found at {path}")
            images.append(None)
    
    # Skip if no valid images
    if not any(images):
        print(f"Skipping empty page: {output_path}")
        return
    
    # Calculate dimensions for layout
    if len(scene_paths) == 3 and all(images):
        # Special layout for 3 images: two horizontal stacked left, one vertical right
        left_width = HORIZONTAL_SIZE[0]
        right_width = VERTICAL_SIZE[0]
        
        # Calculate left column height (two horizontal images + text + padding)
        text1 = wrap_text(scene_texts[0], font, HORIZONTAL_SIZE[0])
        text2 = wrap_text(scene_texts[1], font, HORIZONTAL_SIZE[0])
        text_height1 = len(text1) * (font.getbbox("A")[3] + 5)
        text_height2 = len(text2) * (font.getbbox("A")[3] + 5)
        
        left_height = (HORIZONTAL_SIZE[1] + text_height1 + 10 + 
                      HORIZONTAL_SIZE[1] + text_height2 + 10 + PADDING)
        
        # Right column height (vertical image + text)
        text3 = wrap_text(scene_texts[2], font, VERTICAL_SIZE[0])
        text_height3 = len(text3) * (font.getbbox("A")[3] + 5)
        right_height = VERTICAL_SIZE[1] + text_height3 + 10
        
        total_width = left_width + right_width + 3 * PADDING
        total_height = max(left_height, right_height) + 2 * PADDING
        
        canvas = Image.new("RGB", (total_width, total_height), BACKGROUND_COLOR)
        draw = ImageDraw.Draw(canvas)
        
        # Left column - first horizontal image
        y_offset = PADDING
        img = images[0]
        box_height = img.height + text_height1 + 10
        draw.rectangle(
            [PADDING, y_offset, PADDING + img.width, y_offset + box_height],
            outline=BORDER_COLOR, width=BORDER_WIDTH
        )
        canvas.paste(img, (PADDING, y_offset))
        
        # Text for first image
        text_y = y_offset + img.height + 5
        for line in text1:
            text_width = draw.textlength(line, font=font)
            text_x = PADDING + (img.width - text_width) // 2
            draw.text((text_x, text_y), line, fill=TEXT_COLOR, font=font)
            text_y += font.getbbox("A")[3] + 5
        
        # Left column - second horizontal image
        y_offset += img.height + text_height1 + 10 + PADDING
        img = images[1]
        box_height = img.height + text_height2 + 10
        draw.rectangle(
            [PADDING, y_offset, PADDING + img.width, y_offset + box_height],
            outline=BORDER_COLOR, width=BORDER_WIDTH
        )
        canvas.paste(img, (PADDING, y_offset))
        
        # Text for second image
        text_y = y_offset + img.height + 5
        for line in text2:
            text_width = draw.textlength(line, font=font)
            text_x = PADDING + (img.width - text_width) // 2
            draw.text((text_x, text_y), line, fill=TEXT_COLOR, font=font)
            text_y += font.getbbox("A")[3] + 5
        
        # Right column - vertical image
        x_offset = PADDING * 2 + left_width
        y_offset = PADDING
        img = images[2]
        box_height = img.height + text_height3 + 10
        draw.rectangle(
            [x_offset, y_offset, x_offset + img.width, y_offset + box_height],
            outline=BORDER_COLOR, width=BORDER_WIDTH
        )
        canvas.paste(img, (x_offset, y_offset))
        
        # Text for vertical image
        text_y = y_offset + img.height + 5
        for line in text3:
            text_width = draw.textlength(line, font=font)
            text_x = x_offset + (img.width - text_width) // 2
            draw.text((text_x, text_y), line, fill=TEXT_COLOR, font=font)
            text_y += font.getbbox("A")[3] + 5
    
    else:
        # For 1 or 2 images, use simple vertical stack
        total_width = HORIZONTAL_SIZE[0] + 2 * PADDING
        total_height = PADDING
        
        text_heights = []
        for i, (img, text) in enumerate(zip(images, scene_texts)):
            if img:
                lines = wrap_text(text, font, HORIZONTAL_SIZE[0])
                text_heights.append(len(lines) * (font.getbbox("A")[3] + 5))
                total_height += HORIZONTAL_SIZE[1] + text_heights[-1] + 10 + PADDING
            else:
                text_heights.append(0)
        
        canvas = Image.new("RGB", (total_width, total_height), BACKGROUND_COLOR)
        draw = ImageDraw.Draw(canvas)
        
        y_offset = PADDING
        for i, (img, text) in enumerate(zip(images, scene_texts)):
            if not img:
                continue
                
            img = img.resize(HORIZONTAL_SIZE)
            box_height = img.height + text_heights[i] + 10
            draw.rectangle(
                [PADDING, y_offset, PADDING + img.width, y_offset + box_height],
                outline=BORDER_COLOR, width=BORDER_WIDTH
            )
            canvas.paste(img, (PADDING, y_offset))
            
            text_y = y_offset + img.height + 5
            lines = wrap_text(text, font, img.width)
            for line in lines:
                text_width = draw.textlength(line, font=font)
                text_x = PADDING + (img.width - text_width) // 2
                draw.text((text_x, text_y), line, fill=TEXT_COLOR, font=font)
                text_y += font.getbbox("A")[3] + 5
            
            y_offset += img.height + text_heights[i] + 10 + PADDING
    
    # Save output
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    canvas.save(output_path)
    print(f"Created: {output_path}")

def create_book(scenes):
    """Create comic pages from scenes"""
    # Get all scene images from the comic_images directory
    try:
        image_files = sorted(
            [os.path.join(COMIC_IMAGES_DIR, f) 
             for f in os.listdir(COMIC_IMAGES_DIR) 
             if f.startswith('scene') and f.endswith('.png')],
            key=lambda x: int(os.path.basename(x)[5:-4])
        )
        
        if not image_files:
            raise FileNotFoundError(f"No scene images found in {COMIC_IMAGES_DIR}")
            
        if len(scenes) < len(image_files):
            print(f"Warning: More images ({len(image_files)}) than scene descriptions ({len(scenes)})")
            # Pad with empty texts if needed
            scenes += [""] * (len(image_files) - len(scenes))
        
        # Process images in groups of 3
        for group_idx in range(0, len(image_files), 3):
            group_end = min(group_idx + 3, len(image_files))
            scene_group = image_files[group_idx:group_end]
            text_group = scenes[group_idx:group_end]
            
            output_path = f"output/{OUTPUT_PREFIX}{group_idx//3 + 1}.png"
            create_comic_page(scene_group, text_group, output_path)
            
    except Exception as e:
        print(f"Error creating comic book: {str(e)}")
        raise

if __name__ == "__main__":
    create_book([
        "Scene 1: Description for first scene",
        "Scene 2: Description for second scene",
        "Scene 3: Description for third scene",
        "Scene 4: Description for fourth scene",
        "Scene 5: Description for fifth scene",
        "Scene 6: Description for sixth scene",
        "Scene 7: Description for seventh scene",
        "Scene 8: Description for eighth scene",
        "Scene 9: Description for ninth scene",
        "Scene 10: Description for tenth scene"
    ])
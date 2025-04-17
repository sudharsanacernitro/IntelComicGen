import os
import img2pdf

# Configuration
image_folder = "./output"  # Folder containing your images

# Get all image files from folder
def pdfConvert(output):
    image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) 
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # Sort images by name
    image_files.sort()

    # Create PDF
    with open(output, "wb") as f:
        f.write(img2pdf.convert(image_files))

    print(f"PDF created with {len(image_files)} images: {output}")
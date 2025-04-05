import os
import img2pdf

# Configuration
image_folder = "./output"  # Folder containing your images
output_pdf = "comic.pdf"

# Get all image files from folder
def pdfConvert():
    image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) 
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # Sort images by name
    image_files.sort()

    # Create PDF
    with open(output_pdf, "wb") as f:
        f.write(img2pdf.convert(image_files))

    print(f"PDF created with {len(image_files)} images: {output_pdf}")
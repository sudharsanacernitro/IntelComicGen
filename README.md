🕵️ ComicBook Generator with ComfyUI, Swarm, Flux & Ollama

This Python-based project automatically generates a comic book using:

    Swarm Agents for story generation

    ComfyUI with Flux + Flux Pulid for consistent image creation

    Ollama + Qwen2.5 coder for AI-powered logic

    Pillow & img2pdf for rendering images and compiling PDFs

📦 Installation

Clone this repository

    git clone https://github.com/sudharsanacernitro/IntelComicGen.git
    cd IntelComicGen

Create a virtual environment (optional but recommended)

    python3 -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate     # Windows

Install the dependencies

    pip install -r requirements.txt

📜 Requirements

List of required Python packages:

swarm
openai
pillow
img2pdf
websocket-client
urllib

You can install them via:

pip install swarm openai pillow img2pdf

🚀 Usage

To generate a comic book, simply run:

python main.py --story "Detective JamesBond and his case" --genre "crime" --server "9f41-103-196-28-166.ngrok-free.app"

Arguments:

    --story: The base storyline or prompt

    --genre: The genre (e.g., crime, horror, fantasy, sci-fi)

    --server: The ComfyUI inference server URL (e.g., ngrok tunnel to localhost)

🧠 How It Works

    Story Creation
    Uses Swarm agents powered by Ollama to generate a structured 10-scene story.

    Character Description
    Each unique character is described to maintain consistency in appearance.

    Image Generation
    Images are generated scene-by-scene using ComfyUI + Flux Pulid models.

    Title Card & Text
    A custom title page is created. Scene images are captioned and bordered.

    Compilation
    Images are converted to high-res comic pages and exported as a PDF.

📘 Output Example

    Comic Pages: output/comic_page_1.png, comic_page_2.png, ...

    Final PDF: comic.pdf

💡 Notes

    Make sure your ComfyUI server is running and accessible via the provided URL.

    You can modify story_creation.py to adjust tone, structure, or formatting of stories.
    
Requirements

24GB VRAM required - comfyui(flux)
RAM 8GB or GPU - ollama

🛠 TODO

Add character name consistency checker

Add voice-over generation

    Export as EPUB / web comic viewer

📃 License

MIT License — feel free to use, remix, and share.

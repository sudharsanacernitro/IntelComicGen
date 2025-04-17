import streamlit as st
from story_creation import run_creation
from character_description import SceneCreation
from img_upload import ComfyUIClient
from comic_images.test1 import create_book
from imgToPdf import pdfConvert
from TitleCard import title
import os

def main():
    st.set_page_config(page_title="Comic Book Generator", layout="wide")
    st.title("🎨 Comic Book Generator")

    col1, col2 = st.columns(2)

    with col1:
        # Input fields in the left column
        story = st.text_area("✍️ Enter your story/theme", help="Main storyline of the comic")
        genre = st.selectbox("🎭 Choose a genre", ["Fantasy", "Sci-Fi", "Adventure", "Mystery", "Romance", "Horror"])
        output_file = st.text_input("📄 Output PDF file name", value="comic.pdf")
        server = st.text_input("🌐 ComfyUI server address (e.g., http://127.0.0.1:8188)")
        input_image = st.file_uploader("🖼️ Upload base character image", type=["jpg", "jpeg", "png"])

        # ✅ Show image preview
        if input_image:
            st.image(input_image, caption="Uploaded Character Image Preview", use_column_width=True)

        generate_btn = st.button("🚀 Generate Comic")

    if generate_btn:
        if not story or not genre or not server:
            st.error("Please fill in all required fields.")
            return

        with st.spinner("Creating comic scenes..."):
            # Scene and Title
            scene_creator = SceneCreation()
            scenes = run_creation(story, genre)
            title(story)

            # Image generation client
            img_gen_client = ComfyUIClient(server)
            workflow = img_gen_client.load_workflow()

            if input_image:
                # image_path = os.path.join("uploaded_images", input_image.name)
                # with open(image_path, "wb") as f:
                #     f.write(input_image.getvalue())
                # st.success(f"Uploaded image saved as {image_path}")
                image_path = "201.jpeg"
            else:
                image_path = "201.jpeg"  # Default image

            with col2:
                for idx, scene in enumerate(scenes, start=1):
                    scene_desc = scene_creator.get_scene_description(scene)
                    workflow = img_gen_client.update_workflow_with_image(workflow, scene, idx % 3 == 0)
                    
                    response = img_gen_client.queue_prompt(workflow)
                    prompt_id = response['prompt_id']
                    
                    image = img_gen_client.get_image(prompt_id)
                    if image:
                        save_path = f"comic_images/scene{idx}.png"
                        img_gen_client.save_image(image, save_path)
                        st.image(save_path, caption=f"Scene {idx}", use_column_width=True)
                    
                    st.markdown(f"**Scene {idx} Description:** {scene_desc}")

            create_book(scenes)
            pdfConvert(output_file)
            st.success("✅ Comic Book created successfully!")
            st.download_button("📥 Download PDF", data=open(output_file, "rb"), file_name=output_file)

if __name__ == "__main__":
    main()

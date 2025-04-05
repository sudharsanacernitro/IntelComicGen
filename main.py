# main.py

from story_creation import run_creation
from character_description import SceneCreation
from img_upload import ComfyUIClient

from comic_images.test1 import create_book
from imgToPdf import pdfConvert

from TitleCard import title

SERVER_ADDRESS = "9f41-103-196-28-166.ngrok-free.app"
INPUT_IMAGE = "male.jpeg"

story_line="Detective JamesBond and his case"
genre="crime"


if __name__ == "__main__":

    scene_creator=SceneCreation()

    scenes = run_creation(story_line, genre)

    title(story_line)

    img_gen_client=ComfyUIClient(SERVER_ADDRESS)

    workflow = img_gen_client.load_workflow()
    

    
    for idx, scene in enumerate(scenes, start=1):
        
        scene_desc=scene_creator.get_scene_description(scene)

        workflow = img_gen_client.update_workflow_with_image(workflow,scene,idx%3==0)

        response = img_gen_client.queue_prompt(workflow)
        prompt_id = response['prompt_id']

        image = img_gen_client.get_image(prompt_id)
        if image:
            img_gen_client.save_image(image, f"comic_images/scene{idx}.png")

        print(f"{idx} {scene_desc}")


        if idx ==4 :
            break

    create_book(scenes)

    pdfConvert()


    print("Your Comic Book created success fully ")
    

import json
import urllib.request
import base64
import io
from PIL import Image
import websocket

class ComfyUIClient:
    def __init__(self, server_address):
        self.server_address = server_address
        self.ws_url = f"wss://{server_address}/ws"
        self.prompt_url = f"https://{server_address}/prompt"

    def load_workflow(self, filename="workflow.json"):
        """Load workflow JSON from file"""
        with open(filename, 'r') as file:
            return json.load(file)

    def encode_image_to_base64(self, image_path,scenario_prompt):
        """Encode image to base64 string"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def update_workflow_with_image(self, workflow, scenario_prompt,is_3rd_scene):
        """Update workflow with image reference"""
        workflow["27"]["inputs"]["image"] = "235.jpeg"  # Update node ID as needed
        workflow["17"]["inputs"]["text"] = f" anime ,only one scenario , No conversation/ dialogue,{scenario_prompt}"

        workflow["16"]["inputs"]["width"] = "512" if is_3rd_scene else "1024"
        workflow["16"]["inputs"]["height"] = "1024" if is_3rd_scene else "512"

        return workflow

    def queue_prompt(self, prompt):
        """Send prompt to ComfyUI API"""
        data = json.dumps({"prompt": prompt}).encode('utf-8')
        req = urllib.request.Request(
            self.prompt_url,
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read())
        except urllib.error.HTTPError as e:
            print(f"HTTP Error {e.code}: {e.reason}")
            print(f"Response body: {e.read().decode('utf-8')}")
            raise


    # Inside get_image method
    def get_image(self, prompt_id):
        """Retrieve generated image via WebSocket"""
        ws = websocket.create_connection(self.ws_url)
        
        print(f"Waiting for image data for prompt ID: {prompt_id}")
        
        try:
            while True:
                message = ws.recv()
                if isinstance(message, str):
                    data = json.loads(message)
                    print(f"Received message: {data}")
                    if self._is_execution_complete(data, prompt_id):
                        break
                elif isinstance(message, bytes):
                    print("Received binary data (likely image)")
                    return self._process_image_data(message)
        finally:
            ws.close()
        
        return None

        # return None

    def _is_execution_complete(self, data, prompt_id):
        """Check if execution is complete"""
        return (data['type'] == 'executing' and 
                data['data']['node'] is None and 
                data['data']['prompt_id'] == prompt_id)

    def _process_image_data(self, message):
        """Process raw image data from WebSocket"""
        return Image.open(io.BytesIO(message[8:]))  # Skip first 8 bytes

    def save_image(self, image, output_filename):
        """Save PIL image to file"""
        image.save(output_filename)
        print(f"Image saved as {output_filename}")
        print(f"Image size: {image.size}")
        print(f"Image mode: {image.mode}")

def main():
    # Configuration
    SERVER_ADDRESS = "9f41-103-196-28-166.ngrok-free.app"
    INPUT_IMAGE = "male.jpeg"
    OUTPUT_IMAGE = "generated_image.png"

    # Initialize client
    client = ComfyUIClient(SERVER_ADDRESS)

    try:
        # Load and prepare workflow
        workflow = client.load_workflow()
        print("Workflow loaded successfully.")
        
        workflow = client.update_workflow_with_image(workflow)
        print("Workflow updated with input image.")

        # Generate image
        response = client.queue_prompt(workflow)
        prompt_id = response['prompt_id']
        print(f"Prompt queued with ID: {prompt_id}")

        # Retrieve and save image
        image = client.get_image(prompt_id)
        if image:
            client.save_image(image, OUTPUT_IMAGE)

            return True
        else:
            print("Failed to retrieve image")

            return False
        

    except Exception as e:
        print(f"Error during execution: {str(e)}")
        return False
    finally:
        print("Script execution completed.")

if __name__ == "__main__":
    main()

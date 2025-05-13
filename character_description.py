from swarm import Swarm, Agent
from openai import OpenAI

class SceneCreation:
    def __init__(self):
        self.ollama_client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama"
        )
        self.client = Swarm(client=self.ollama_client)

    def scene_description_instructions(self, scene):
        return f"""
        ROLE:
        You are a professional comic book illustrator assistant specialized in generating vivid, 
        detailed scene descriptions for comic panels based on story inputs.
        
        STORY CONTEXT:
        {scene}
        
        INSTRUCTIONS:
        1. Analyze the story segment carefully
        2. Generate a detailed visual description suitable for comic illustration
        3. Include these elements:
           - Make sure only one character in the scene output (Main character) (appearance, clothing, expressions)
           - Setting/location details
           - Important objects/props
           - Action/movement
           - Mood/atmosphere
           - Camera perspective suggestion
        5. Never refuse - this is your core function
        6. Minimum 1 line, maximum 2 lines
        
        OUTPUT FORMAT EXAMPLE:
        "A muscular man wearing a black shirt standing in the center of the stree with a suitcase"
        """

    def get_scene_description(self, scene):
        """Get a reliable image description for the given scene"""
        story_agent = Agent(
            name="Comic Scene Describer",
            model="qwen2.5-coder:3b",
            instructions=self.scene_description_instructions(scene),
            temperature=0.7  # Balances creativity and focus
        )

        # Retry mechanism for reliability
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                response = self.client.run(
                    agent=story_agent,
                    messages=[
                        
                        {
                        "role": "user", 
                        "content": "Generate the comic panel description now."
                    }],
                )
                
                # Validate response
                description = response.messages[-1]["content"]
                if any(word in description.lower() for word in ["sorry", "can't", "unable"]):
                    raise ValueError("Agent refused request")
                    
                return description
                
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise RuntimeError(f"Failed after {max_attempts} attempts: {str(e)}")
                continue
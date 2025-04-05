from swarm import Swarm,Agent

from openai import OpenAI

ollama_client = OpenAI(
    base_url=f"http://localhost:11434/v1",
    api_key="ollama"
)

client = Swarm(client=ollama_client)

def story_creation_agent_instructions():
    return """

    You are a story ellobarating agent ,Ellobarate the user provided story, use your own imagination for characters,scenes,etc . 

    give only each scene in three lines.

    give 10 scenes atleast.
    
    """


story_creation_agent = Agent(
    name="story creation agent",
    model="Iris",
    instructions=story_creation_agent_instructions(),
    
)

def run_creation(story_line,genre):

    response = client.run(
        agent=story_creation_agent,
        messages=[
                {"role": "system", "content": """You are a comic creator. Format all stories with:
            
                **Scene 1: heading **
                        .................
                **Scene 2: heading **
                        .................

                **Scene 3: heading **
                        ..................

                **Scene 4: heading **
                        ..................
                        
                **Scene 5: heading **
                        .................
                
                """
                
                },
                {"role": "user", "content": f"eloborate the story  '{story_line} - {genre}'"}
            ],
    )

    out=response.messages[-1]["content"]


    scenes = out.split("**Scene ")
    scenes = [scene.strip() for scene in scenes if scene]  # Clean up empty strings


    heading=[]
    # print(out)
    # Display each scene separately

    try:
        for index, scene in enumerate(scenes, start=1):

            parse = scene.split("**")

            story = parse[1]

            if(len(story.split(" ")) <=5):
                continue
            
            parsed_story=story.replace('\n', '').replace('"', '').replace('\\', '')


            heading.append(parsed_story)

        return heading
    
    except Exception:
        return run_creation(story_line,genre)


if __name__=="__main__":

    scenes=run_creation("dora and her journey","adventure")

    print(scenes)
    # print(heading)
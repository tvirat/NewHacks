import os

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()


class DialogueGenerator:

    def __init__(self):
        self.client = OpenAI(
            # This is the default and can be omitted
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

    def generate_dialogue(self, prompt: str):
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system",
                 "content": "You are a NPC in a fantasy side-scrolling game. You are in a village and you need to talk to the player."},
                {"role": "user", "content": prompt}
            ],
            model="gpt-4o-mini",
            max_completion_tokens=150
        )
        return response.choices[0].message.content
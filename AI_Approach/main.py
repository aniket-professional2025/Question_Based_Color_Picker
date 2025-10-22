# Importing Required Packages
import json
from openai import OpenAI
import os
from dotenv import load_dotenv
print("[DEBUG] Libraries Imported Successfully")

# Loading Environmental Variables
load_dotenv()
print("[DEBUG] Environmental Variables are Loaded Sucessfully")

# Load Your JSON data
with open("color_data.json", "r", encoding = "utf-8") as f:
    DATA = json.load(f)
print("[DEBUG] JSON data is loaded in read mode")

# Setting The OpenAi Client
key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = key)
print("[DEBUG] Openai Client is Set Successfully")

# Define the Color Recommender Function
def get_color_recommendations(zodiac = None, gems = None, nature = None, mood = None, lighting = None, personality = None, themes = None, vaastu = None, room = None):

    # Normalize the User Inputs
    user_inputs = {
        "zodiac": zodiac.lower() if zodiac else None,
        "gems": gems.lower() if gems else None,
        "nature": nature.lower() if nature else None,
        "mood": mood.lower() if mood else None,
        "natural lighting": lighting.lower() if lighting else None,
        "personality": personality.lower() if personality else None,
        "themes": themes.lower() if themes else None,
        "vaastu": vaastu.lower() if vaastu else None,
        "room": room.lower() if room else None,
    }

    # Setting the System prompt
    system_prompt = """
    You are expert in color recommendation by analysing different traits of user. You are given:
    1. A JSON dataset mapping different categories (zodiac, gems, nature, etc. and their sub-categories like capricorn, pearl etc.) to colors.
    2. User selections across these categories and sub-categories

    TASK:
    After analysing the user selections and the JSON data provided
    - Select exactly 5 colors (from the JSON only, no outside colors).
    - Output must be in JSON with:
        {
          "colors": [
            {"name": "<color name>", "hex": "<hex code>"},
            ...
          ],
          "explanation": "<short reason why these colors were chosen>"
        }
    """

    # Setting The User Prompt
    user_prompt = f"""
    JSON Data:
    {json.dumps(DATA)}

    User Inputs:
    {json.dumps(user_inputs)}

    Please return the best 5 matching colors and explanation after analysing the JSON data and User Inputs carefully.
    """

    # Getting the Response
    response = client.chat.completions.create(
        model = "gpt-4.1",
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format = {"type": "json_object"}, # Force JSON response
        temperature = 0.7
    )

    # Parse the response
    reply = response.choices[0].message.content

    # # GPT should return valid JSON
    result = json.loads(reply)  

    print("[DEBUG] The function runs Successfully")

    return result
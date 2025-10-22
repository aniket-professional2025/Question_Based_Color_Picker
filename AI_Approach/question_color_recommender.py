# Importing Required Packages
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
print("[DEBUG] Libraries loaded succesfully")

# export OPENAI_API_KEY="your_key"
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
MODEL_Q = "gpt-4.1"   # for generating questions
MODEL_REC = "gpt-4.1" # for final recommendations
PALETTE_PATH = "color_data.json"
print("[DEBUG] Configuration files are set")

# Setting the OpenAI Client
client = OpenAI(api_key = api_key)
print("[DEBUG] The Openai Client is Set")

# LOAD DATA 
with open(PALETTE_PATH, "r", encoding = "utf-8") as f:
    palette = json.load(f)
print("[DEBUG] Data is Loaded in read mode")

# GPT HELPERS FUNCTION: Generate Question
def generate_questions(palette_json):
    
    # (taken only from the JSON keys/values) with the options section
    system_prompt = """
    You are a color recommendation assistant.
    Look at the given JSON data (which contains Berger color palettes with keys like room, themes, mood, natural lighting, vaastu).
    Generate exactly 5 multiple-choice questions to ask the USER directly
    - Questions must be phrased in a natural, user-friendly way (e.g., "What is the mood you want for your room?" instead of "Which palette is associated with mood X").
    - For any option that has multiple sub-options (like zodiac signs, moods, themes), **list all sub-options explicitly**.
    - Each question must have:
        - id: a short identifier (like q1, room, theme, etc.)
        - text: the question wording
        - options: an array of all possible options
    - You can include options that are not in the JSON if they are important for selecting colors.

    Output only valid JSON:
    {
        "questions":[
            {
            "id": "q1", 
            "text": "...", 
            "options" :["...","...","..."]
            }, 
            ...
        ]
    }
    """
    user_prompt = "Here is the palette JSON:\n" + json.dumps(palette_json)

    resp = client.chat.completions.create(
        model = MODEL_Q,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature = 0.7, # some randomness so questions vary
        response_format = {"type": "json_object"}
    )
    raw = resp.choices[0].message.content    
    try:
        data = json.loads(raw)
        return data["questions"]
    except Exception:
        # fallback: try to extract the JSON substring
        start = raw.find("{")
        end = raw.rfind("}") + 1
        data = json.loads(raw[start:end])
    
    if "questions" in data:
        return data["questions"]
    else: 
        raise ValueError("Model output missing 'questions' key")
print("[DEBUG] The function to generate questions with their options is set succesfully")

# GPT HELPERS FUNCTION: Generate Color Recommendations
def get_recommendations(palette_json, answers):
    system_prompt = """
    You are a Berger paint color recommendation engine for Indian Users who are interested in painting their homes

    Process:
    1. Carefully analyze the user's answers (about mood, lighting, room type, vaastu, preferences)
    2. Look inside the palette JSON. Each sub-section (like "Free Spirit") may have multiple colors.
    3. For the sections relevant to the user's answers, evaluate **all candidate colors**, not just the first one.
    4. Rank them with your understading, thinking from an user perspective and then select the TOP 3 colors overall.
    5. Output JSON with this schema
    {
        "analysis": "<A consize but crisp logical explanation on how the user selection guided the color recommendation system>", 
        "colors": [
        {"name": "<color name>", "hex": "<hex code>"},
        ...
        ],
        "explanation": "<A consize but crisp reason why these colors were chosen>"
    }

    Rules:
    - Use ONLY colors found in the palette JSON.
    - Do NOT always pick the first color. Consider all in the relevant section(s).
    - Return exactly {top_k} final colors.
    """
    user_prompt = (
        "User answers:\n" + json.dumps(answers, indent = 2) +
        "\n\nPalette JSON:\n" + json.dumps(palette_json)
    )

    resp = client.chat.completions.create(
        model=MODEL_REC,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature = 0.3, # more deterministic
        response_format = {"type": "json_object"}  
    )
    raw = resp.choices[0].message.content
    
    # Get the result
    result = json.loads(raw)

    print("[DEBUG] The Function runs successfully")

    return result
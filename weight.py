# Importing Required Packages
import json
from collections import defaultdict

# Load the JSON data (replace with open('data.json') if stored externally)
with open("color_data.json", "r") as f:
    color_data = json.load(f)

# Define the Function to get Importance weight based color recommendations
def get_recommendations(space: str, mood: str, lighting: str, personality: str, vastu_choice: str, number_of_colors: int, vastu_direction: str = None, weights: dict = None):

    """
    Fetch top 3 recommended colors based on weighted scoring
    weights: dict with keys ['space', 'mood', 'lighting', 'personality', 'vaastu']
    values should sum to 1. Example:
        {
            "space": 0.4,
            "mood": 0.25,
            "lighting": 0.15,
            "personality": 0.1,
            "vaastu": 0.1
        }

    """
    # Default weights if not provided
    if weights is None:
        weights = {
            "space": 0.4,
            "mood": 0.25,
            "lighting": 0.15,
            "personality": 0.1,
            "vaastu": 0.1
        }

    # Accumulate weighted scores per color
    color_scores = defaultdict(float)  

    all_colors = []

    # ROOM
    room_key = space.lower()
    if room_key in color_data["space"]:
        for item in color_data["space"][room_key]:
            color_scores[item["name"]] += weights.get("space", 0)
        all_colors += color_data["space"][room_key]

    # MOOD
    mood_key = mood.lower()
    if mood_key in color_data["mood"]:
        for item in color_data["mood"][mood_key]:
            color_scores[item["name"]] += weights.get("mood", 0)
        all_colors += color_data["mood"][mood_key]

    # NATURAL LIGHTING
    light_key = lighting.lower()
    if light_key in color_data["natural lighting"]:
        for item in color_data["natural lighting"][light_key]:
            color_scores[item["name"]] += weights.get("lighting", 0)
        all_colors += color_data["natural lighting"][light_key]

    # PERSONALITY
    personality_key = personality.lower()
    if personality_key in color_data["personality"]:
        for item in color_data["personality"][personality_key]:
            color_scores[item["name"]] += weights.get("personality", 0)
        all_colors += color_data["personality"][personality_key]

    # VAASTU (only for first two options)
    if vastu_choice.lower() in ["yes, strictly follow vaastu", "yes, but flexible"]:
        direction = None

        # Priority 1: Use user-selected vastu_direction (if provided)
        if vastu_direction and vastu_direction.lower() in color_data["vaastu"]:
            direction = vastu_direction.lower()

        # Priority 2: Otherwise, infer from lighting text
        else:
            for d in ["east", "west", "north", "south", "south east", "south west", "north east", "north west"]:
                if d in lighting.lower():
                    direction = d
                    break
        
        if direction and direction in color_data["vaastu"]:
            for item in color_data["vaastu"][direction]:
                color_scores[item["name"]] += weights.get("vaastu", 0)
            all_colors += color_data["vaastu"][direction]

    # Sort colors by cumulative weighted score
    sorted_colors = sorted(color_scores.items(), key=lambda x: x[1], reverse = True)

    # Return top 3 recommended colors with scores
    top_colors = [{"color": name, "score": round(score, 2)} for name, score in sorted_colors[:number_of_colors]]
    final_output = []

    for item_dict in top_colors:
        name = item_dict["color"]
        score = item_dict["score"]
        # find matching hex from all_colors
        for color_item in all_colors:
            if color_item["name"] == name:
                final_output.append({"color": name, "hex": color_item["hex"], "score": score})
                break

    return all_colors, final_output
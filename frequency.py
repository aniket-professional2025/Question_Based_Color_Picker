# Importing Required Packages
import json
from collections import Counter

# Load the JSON data (replace with open('data.json') if stored externally)
with open("color_data.json", "r") as f:
    color_data = json.load(f)

# Define the Function to get frequency based color recommendations
def get_recommendations(space: str, mood: str, lighting: str, personality: str, vastu_choice: str, number_of_colors: int,  vastu_direction: str = None):

    """
    Fetch top 3 recommended colors based on frequency of occurrence.
    """

    all_colors = []

    # ROOM
    room_key = space.lower()
    if room_key in color_data["space"]:
        all_colors += color_data["space"][room_key]

    # MOOD
    mood_key = mood.lower()
    if mood_key in color_data["mood"]:
        all_colors += color_data["mood"][mood_key]

    # NATURAL LIGHTING
    light_key = lighting.lower()
    if light_key in color_data["natural lighting"]:
        all_colors += color_data["natural lighting"][light_key]

    # PERSONALITY
    personality_key = personality.lower()
    if personality_key in color_data["personality"]:
        all_colors += color_data["personality"][personality_key]

    # VAASTU (only for first two options)
    if vastu_choice.lower() in ["yes, strictly follow vaastu", "yes, but flexible"]:
        direction = None

        # Priority 1: Use user-selected vastu_direction (if provided)
        if vastu_direction and vastu_direction.lower() in color_data["vaastu"]:
            direction = vastu_direction.lower()

        # Priority 2: Otherwise, infer from lighting text
        else:
            if "east" in lighting.lower():
                direction = "east"
            elif "west" in lighting.lower():
                direction = "west"
            elif "north" in lighting.lower():
                direction = "north"
            elif "south" in lighting.lower():
                direction = "south"
            elif "south east" in lighting.lower():
                direction = "south east"
            elif "south west" in lighting.lower():
                direction = "south west"
            elif "north east" in lighting.lower():
                direction = "north east"
            elif "north west" in lighting.lower():
                direction = "north west"
        
        if direction and direction in color_data["vaastu"]:
            all_colors += color_data["vaastu"][direction]

    # Combine frequencies
    color_counter = Counter([item["name"] for item in all_colors])
    top_colors = color_counter.most_common(number_of_colors)

    # Prepare output with hex codes
    final_output = []
    for name, freq in top_colors:
        for item in all_colors:
            if item["name"] == name:
                final_output.append({"name": name, "hex": item["hex"], "frequency": freq})
                break

    return all_colors, final_output
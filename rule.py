# Import necessary libraries
import json

# Load color data from JSON file
with open("color_data.json", "r") as f:
    color_data = json.load(f)

# Define the Rule-Based Recommendation Function
def rule_based_recommendations(space: str, mood: str, lighting: str, personality: str, vastu_choice: str, vastu_direction: str = None, number_of_colors: int = 3):
    """
    Rule-Based Hierarchy Algorithm
    Priority Order: lighting → space → mood → personality → vaastu
    Returns:
        - all_colors_fetched: list of all colors fetched from user inputs
        - top recommended colors (name + hex)
    """
    
    all_colors_fetched = []  # store all colors fetched from each category
    
    # Helper function to get colors from a category key
    def get_colors(category, key):
        key = key.lower()
        if key in color_data[category]:
            return color_data[category][key]  # return full dicts
        return []
    
    # Step 1: Lighting
    lighting_colors = get_colors("natural lighting", lighting)
    all_colors_fetched += lighting_colors
    filtered_colors = set(item["name"] for item in lighting_colors)
    
    # Step 2: Space
    space_colors = get_colors("space", space)
    all_colors_fetched += space_colors
    filtered_colors = filtered_colors & set(item["name"] for item in space_colors) if filtered_colors else set(item["name"] for item in space_colors)
    
    # Step 3: Mood
    mood_colors = get_colors("mood", mood)
    all_colors_fetched += mood_colors
    filtered_colors = filtered_colors & set(item["name"] for item in mood_colors) if filtered_colors else set(item["name"] for item in mood_colors)
    
    # Step 4: Personality
    personality_colors = get_colors("personality", personality)
    all_colors_fetched += personality_colors
    filtered_colors = filtered_colors & set(item["name"] for item in personality_colors) if filtered_colors else set(item["name"] for item in personality_colors)
    
    # Step 5: Vaastu
    if vastu_choice.lower() in ["yes, strictly follow vaastu", "yes, but flexible"]:
        direction = None
        if vastu_direction and vastu_direction.lower() in color_data["vaastu"]:
            direction = vastu_direction.lower()
        else:
            # Try to infer from lighting
            for d in ["east", "west", "north", "south", "south east", "south west", "north east", "north west"]:
                if d in lighting.lower():
                    direction = d
                    break
        if direction and direction in color_data["vaastu"]:
            vaastu_colors = color_data["vaastu"][direction]
            all_colors_fetched += vaastu_colors
            filtered_colors = filtered_colors & set(item["name"] for item in vaastu_colors)
    
    # Create lookup dict for HEX codes
    hex_lookup = {item["name"]: item["hex"] for item in all_colors_fetched}
    
    # Prepare top N recommended colors
    final_output = [{"name": name, "hex": hex_lookup[name]} for name in filtered_colors if name in hex_lookup]
    
    return all_colors_fetched, final_output[:number_of_colors]
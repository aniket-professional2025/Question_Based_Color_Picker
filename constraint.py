# Import necessary libraries
import json

# Load color data from JSON file
with open("color_data.json", "r") as f:
    color_data = json.load(f)

# Function to get color recommendations based on constraints (intersection-based)
def constraint_satisfaction_recommendations(space, mood, lighting, personality, vastu_choice, vastu_direction=None, number_of_colors=3):
    """
    Constraint Satisfaction Algorithm (Intersection-based)
    Returns colors that satisfy all user constraints simultaneously.
    Also returns all colors considered as dicts: {'name':..., 'hex':...}
    """
    
    all_colors = []  # now store dicts

    # Helper function to fetch color dicts from a category
    def get_colors(category, key):
        key = key.lower()
        if key in color_data[category]:
            return color_data[category][key]  # list of dicts
        return []

    # Fetch colors for each constraint
    space_colors = get_colors("space", space)
    all_colors += space_colors

    mood_colors = get_colors("mood", mood)
    all_colors += mood_colors

    lighting_colors = get_colors("natural lighting", lighting)
    all_colors += lighting_colors

    personality_colors = get_colors("personality", personality)
    all_colors += personality_colors

    # Start intersection based on names
    filtered_colors = set(item["name"] for item in space_colors) & \
                      set(item["name"] for item in mood_colors) & \
                      set(item["name"] for item in lighting_colors) & \
                      set(item["name"] for item in personality_colors)

    # Handle Vaastu
    if vastu_choice.lower() in ["yes, strictly follow vaastu", "yes, but flexible"]:
        direction = vastu_direction.lower() if vastu_direction and vastu_direction.lower() in color_data["vaastu"] else None
        if not direction:
            for d in ["east", "west", "north", "south", "south east", "south west", "north east", "north west"]:
                if d in lighting.lower():
                    direction = d
                    break
        if direction and direction in color_data["vaastu"]:
            vaastu_colors = get_colors("vaastu", direction)
            all_colors += vaastu_colors
            filtered_colors &= set(item["name"] for item in vaastu_colors)

    # Lookup dict for hex
    hex_lookup = {item["name"]: item["hex"] for item in all_colors}

    # Prepare final output
    final_output = [{"color": name, "hex": hex_lookup[name]} for name in filtered_colors if name in hex_lookup]

    return all_colors, final_output[:number_of_colors]
# Import necessary libraries
import json

# Load color data from JSON file
with open("color_data.json", "r") as f:
    color_data = json.load(f)


def mcdm_color_recommendations(space: str, mood: str, lighting: str, personality: str, vastu_choice: str, vastu_direction: str = None, number_of_colors: int = 3):
    """
    Multi-Criteria Decision Making (MCDM) Algorithm
    Each user preference is treated as a criterion.
    Colors are scored based on how many criteria they match.
    The final score = normalized weight based on number of matches.
    """

    # Helper function to safely fetch color dicts for a given category and key
    def get_colors(category, key):
        key = key.lower()
        if key in color_data[category]:
            return color_data[category][key]  # list of dicts with {'name', 'hex'}
        return []

    # Step 1: Gather color sets for each criterion
    space_colors = get_colors("space", space)
    mood_colors = get_colors("mood", mood)
    lighting_colors = get_colors("natural lighting", lighting)
    personality_colors = get_colors("personality", personality)

    # Handle Vaastu (directional constraint)
    vaastu_colors = []
    if vastu_choice.lower() in ["yes, strictly follow vaastu", "yes, but flexible"]:
        direction = vastu_direction.lower() if vastu_direction and vastu_direction.lower() in color_data["vaastu"] else None
        if not direction:
            for d in ["east", "west", "north", "south", "south east", "south west", "north east", "north west"]:
                if d in lighting.lower():
                    direction = d
                    break
        if direction and direction in color_data["vaastu"]:
            vaastu_colors = get_colors("vaastu", direction)

    # Step 2: Combine all unique colors across categories
    all_color_entries = space_colors + mood_colors + lighting_colors + personality_colors + vaastu_colors
    hex_lookup = {c["name"]: c["hex"] for c in all_color_entries}
    unique_colors = set(hex_lookup.keys())

    # Step 3: Assign scores based on matches (weighted equally for now)
    scores = {color: 0 for color in unique_colors}

    # Define equal weights (you can adjust to prioritize certain criteria)
    weights = {
        "space": 1.0,
        "mood": 1.0,
        "lighting": 1.0,
        "personality": 1.0,
        "vaastu": 1.0
    }

    # Increment scores for each criterion the color matches
    for c in unique_colors:
        if any(c == item["name"] for item in space_colors):
            scores[c] += weights["space"]
        if any(c == item["name"] for item in mood_colors):
            scores[c] += weights["mood"]
        if any(c == item["name"] for item in lighting_colors):
            scores[c] += weights["lighting"]
        if any(c == item["name"] for item in personality_colors):
            scores[c] += weights["personality"]
        if any(c == item["name"] for item in vaastu_colors):
            scores[c] += weights["vaastu"]

    # Step 4: Normalize scores (so top color gets 1.0)
    max_score = max(scores.values()) if scores else 1
    for c in scores:
        scores[c] = round(scores[c] / max_score, 2)

    # Step 5: Sort colors by score (descending)
    ranked_colors = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Step 6: Prepare final results with hex codes
    final_output = [{"name": color, "hex": hex_lookup[color], "score": score}
                    for color, score in ranked_colors if color in hex_lookup]

    return all_color_entries, final_output[:number_of_colors]
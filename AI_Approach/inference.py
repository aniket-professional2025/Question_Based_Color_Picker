# Quick Inference on the Function to check if it works or not
from frequency import get_color_recommendations

# Passing the function to user input values
rec = get_color_recommendations(
        zodiac = "Capricorn",
        gems = "Ruby",
        nature = "Beach",
        mood = "Relaxed and Serene",
        lighting = "East Facing Room",
        personality = "Creative",
        themes = "Minimalist",
        vaastu = "North-East",
        room = "Living Room"
    )

# Printing the result
print(rec)
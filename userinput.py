################################ FOR FREQUENCY BASED RECOMMENDATION ################################

user_inputs1 = {
    "space": "Bedroom",
    "mood": "Relaxed and Serene",
    "lighting": "South facing room",
    "personality": "Dreamer",
    "vastu_choice": "Yes, strictly follow vaastu"
}

# Test 2: Vaastu option, explicit user direction Explicit direction
user_inputs2 = {
    "space": "Living Room",
    "mood": "Bold and Dramatic",
    "lighting": "East facing room",
    "personality": "Creative",
    "vastu_choice": "Yes, but flexible",
    "vastu_direction": "north east"  
}

# Test 3: No Vaastu
user_inputs3 = {
    "space": "Balcony",
    "mood": "Cozy and Inviting",
    "lighting": "West facing room",
    "personality": "Analytical",
    "vastu_choice": "No"
}

################################ FOR WEIGHT BASED RECOMMENDATION ################################
user_input = {
    "space" : "Living Room",
    "mood" : "Bold and Dramatic",
    "lighting" : "North facing room",
    "personality" : "Analytical & Practical",
    "vastu_choice" : "Yes, strictly follow Vaastu",
    "weights" : {
        "space": 0.4,
        "mood": 0.25,
        "lighting": 0.15,
        "personality": 0.1,
        "vaastu": 0.1
    }
}



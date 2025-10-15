##################### FOR FREQUENCY BASED RECOMMENDATION #####################

# from frequency import get_recommendations

# # Test 1: Vaastu option, lighting-based direction
# user_inputs1 = {
#     "space": "Bedroom",
#     "mood": "Relaxed and Serene",
#     "lighting": "South facing room",
#     "personality": "Dreamer",
#     "vastu_choice": "Yes, strictly follow vaastu"
# }

# # Test 2: Vaastu option, explicit user direction Explicit direction
# user_inputs2 = {
#     "space": "Living Room",
#     "mood": "Bold and Dramatic",
#     "lighting": "East facing room",
#     "personality": "Creative",
#     "vastu_choice": "Yes, but flexible",
#     "vastu_direction": "north east"  
# }

# # Test 3: No Vaastu
# user_inputs3 = {
#     "space": "Balcony",
#     "mood": "Cozy and Inviting",
#     "lighting": "West facing room",
#     "personality": "Analytical",
#     "vastu_choice": "No"
# }

# all_colors, top_colors = get_recommendations(**user_inputs3, number_of_colors = 3)

# print("All Considered Colors:")
# print("Number of Colors in Consideration:", len(all_colors))
# print("Unique Colors in Consideration:", len(set(c['name'] for c in all_colors)))
# for c in all_colors:
#     print(f"{c['name']} ({c['hex']})")

# print("==========================================================")

# print("Top 3 Recommended Colors:")
# for c in top_colors:
#     print(f"{c['name']} ({c['hex']}) ({c['frequency']})")

##################### FOR IMPORTANCE WEIGHT BASED RECOMMENDATION #####################
# from weight import get_recommendations

# user_input = {
#     "space" : "Living Room",
#     "mood" : "Bold and Dramatic",
#     "lighting" : "North facing room",
#     "personality" : "Analytical",
#     "vastu_choice" : "Yes, strictly follow Vaastu",
#     "weights" : {
#         "space": 0.4,
#         "mood": 0.25,
#         "lighting": 0.15,
#         "personality": 0.1,
#         "vaastu": 0.1
#     }
# }

# all_colors, top_colors = get_recommendations(**user_input, number_of_colors = 3)

# print("All Considered Colors:")
# print("Number of Colors in Consideration:", len(all_colors))
# print("Unique Colors in Consideration:", len(set(c['name'] for c in all_colors)))
# for c in all_colors:
#     print(f"{c['name']} ({c['hex']})")

# print("==========================================================")

# print("Top 3 Recommended Colors:")
# for c in top_colors:
#     print(f"{c['color']} ({c['hex']}) ({c['score']})")

###################### Rule Based Recommendation #####################
# from rule import rule_based_recommendations

# user_inputs = {
#     "space": "Living Room",
#     "mood": "Bold and Dramatic",
#     "lighting": "North facing room",
#     "personality": "Analytical",
#     "vastu_choice": "Yes, but flexible",
#     "vastu_direction": "east"
# }

# all_colors, top_colors = rule_based_recommendations(**user_inputs, number_of_colors = 3)

# print("Top Recommended Colors:")
# print("Number of Colors in Consideration:", len(all_colors))
# print("Unique Colors in Consideration:", len(set(c['name'] for c in all_colors)))
# for c in all_colors:
#     print(f"{c['name']} ({c['hex']})")

# print("==========================================================")

# print("Top 3 Recommended Colors:")
# for c in top_colors:
#     print(f"{c['name']} ({c['hex']})")

####################### Constraint Satisfaction Recommendation #####################
# from constraint import constraint_satisfaction_recommendations

# user_inputs = {
#     "space": "Living Room",
#     "mood": "Bold and Dramatic",
#     "lighting": "East facing room",
#     "personality": "Analytical",
#     "vastu_choice": "Yes, but flexible",
#     "vastu_direction": "east"
# }

# all_colors, top_colors = constraint_satisfaction_recommendations(**user_inputs)

# print("All Considered Colors:")
# print("Number of Colors in Consideration:", len(all_colors))
# print("Unique Colors in Consideration:", len(set(c['name'] for c in all_colors)))
# for c in all_colors:
#     print(f"{c['name']} ({c['hex']})")

# print("==========================================================")
# print("Top Recommended Colors:")
# for c in top_colors:
#     print(f"{c['color']} ({c['hex']})")


##################### Multi-Criteria Decision Making (MCDM) ########################
from mcdm import mcdm_color_recommendations

user_input = {
    "space": "Living Room",
    "mood": "Bold and Dramatic",
    "lighting": "East facing room",
    "personality": "Practical",
    "vastu_choice": "Yes, Strictly Follow Vaastu",
}

all_colors, top_recommendations = mcdm_color_recommendations(**user_input, number_of_colors = 3)

# Print top recommendations
print("All Considered Colors:")
print("Number of Colors in Consideration:", len(all_colors))
print("Unique Colors in Consideration:", len(set(c['name'] for c in all_colors)))
for c in all_colors:
    print(f"{c['name']} ({c['hex']})")

print("==========================================================")

print("Top 3 Recommended Colors:")
for c in top_recommendations:
    print(f"{c['name']} ({c['hex']}) ({c['score']})")
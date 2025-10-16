import json
from flask import Flask, request, jsonify
# from flask_cors import CORS 

# Import all recommendation functions from the provided files
from constraint import *
from frequency import *
from mcdm import *
from rule import *
from weight import *

# Create the Flask instance
app = Flask(__name__)
# CORS(app) # Enable CORS for all routes

# Mapping of algorithm names to their respective function
RECOMMENDATION_METHODS = {
    'frequency': get_recommendations_frequency,
    'weight': get_recommendations_weight,
    'mcdm': mcdm_color_recommendations,
    'rule': rule_based_recommendations,
    'constraint': constraint_satisfaction_recommendations
}

@app.route('/recommend_color', methods=['POST'])

def recommend_color():

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON data in request body"}), 400

    # Required fields and their default values (if applicable)
    required_fields = {
        "space_name": str,
        "mood_name": str,
        "lightning_name": str,
        "personality_name": str,
        "vastu_choice": str,
        "vastu_direction": (str, type(None)), # This field can be a string or None
        "number_of_colors": int 
    }

    # Validate and extract required inputs
    for field, field_type in required_fields.items():
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
        if not isinstance(data[field], field_type):
             return jsonify({"error": f"Invalid type for field: {field}. Expected {field_type.__name__}"}), 400
    
    # Extract optional fields with defaults
    vastu_direction = data.get("vastu_direction")
    # Default to 'weight' if method is not provided or is invalid
    method = data.get("method", 'weight').lower() 

    # Check if the requested method exists
    if method not in RECOMMENDATION_METHODS:
        return jsonify({"error": f"Invalid recommendation method: {method}. Must be one of {list(RECOMMENDATION_METHODS.keys())}"}), 400

    # Extract clean inputs for the function call
    space = data['space_name']
    mood = data['mood_name']
    lighting = data['lightning_name']
    personality = data['personality_name']
    vastu_choice = data['vastu_choice']
    num_colors = data['number_of_colors']

    # Get the selected recommendation function
    recommendation_func = RECOMMENDATION_METHODS[method]

    try:
        # The recommendation functions generally return (all_colors, final_recommendations)
        _, recommended_colors = recommendation_func(
            space = space,
            mood = mood,
            lighting = lighting,
            personality = personality,
            vastu_choice = vastu_choice,
            vastu_direction = vastu_direction,
            number_of_colors = num_colors
        )

        # Structure the successful response
        response = {
            "status": "success",
            "method_used": method,
            "recommended_colors": [
                # Normalize the output keys for consistency, as some modules use 'color' and some use 'name'
                {"color_name": c.get('name') or c.get('color'), "hex_code": c['hex']}
                for c in recommended_colors
            ]
        }
        
        # Add score/frequency/etc if available in the output structure
        if recommended_colors and 'score' in recommended_colors[0]:
             for i, color in enumerate(response['recommended_colors']):
                color['score'] = recommended_colors[i]['score']
        
        elif recommended_colors and 'frequency' in recommended_colors[0]:
             for i, color in enumerate(response['recommended_colors']):
                color['frequency'] = recommended_colors[i]['frequency']
        
        return jsonify(response), 200

    except Exception as e:
        # Catch any unexpected errors during the recommendation logic execution
        return jsonify({"error": f"An internal error occurred during processing: {str(e)}"}), 500

# Standard Flask entry point
if __name__ == '__main__':
    # You can change the port if needed. debug=True enables auto-reloading during development.
    app.run(debug = True, host = '0.0.0.0', port = 5000)

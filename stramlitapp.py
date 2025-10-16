# Importing required libraries
import streamlit as st
import json
from frequency import get_recommendations_frequency 
from mcdm import mcdm_color_recommendations
from weight import get_recommendations_weight 
from rule import rule_based_recommendations
from constraint import constraint_satisfaction_recommendations

# Load the json color data
# NOTE: The color_data.json must be present in the execution environment
with open("color_data.json", "r") as f:
    color_data = json.load(f)

# Function to display the color palette
def display_color_palette(colors, key_prefix):
    cols = st.columns(len(colors))
    for i, color_data in enumerate(colors):
        color_name = color_data.get("color", color_data.get("name", "N/A"))
        hex_code = color_data["hex"]
            
        with cols[i]:
            # Use HTML to display the color patch name and hex
            st.markdown(
                f"""
                <p style="text-align: center; margin-bottom: 5px;font-size: 20px;">
                    <strong style="font-size: 20px;">{color_name}</strong>
                    <br>
                    <span style="font-size: 16px;">{hex_code}</span>
                </p>
                """, unsafe_allow_html=True)
            
            # Use HTML to display the clean color patch
            st.markdown(
                f"""
                <div style="background-color:{hex_code}; padding: 60px; border-radius: 5px; text-align: center; border: 1px solid #ccc;">
                </div>
                """,
                unsafe_allow_html=True
            )

# --- Streamlit Application ---

st.set_page_config(layout = "wide", page_title = "Color Recommendation Systems")
st.title("🏡 Color Recommendation On User Preference")
st.markdown("Select your preferences in the sidebar and click **Submit Your Preference** to see the results from five different recommendation algorithms.")

# Sidebar for User Input
st.sidebar.header("User Preferences")

# 1. Space
space_options = list(color_data.get("space", {}).keys())
space = st.sidebar.selectbox("1. Select Space:", space_options)

# 2. Mood
mood_options = list(color_data.get("mood", {}).keys())
mood = st.sidebar.selectbox("2. Select Desired Mood:", mood_options)

# 3. Personality
personality_options = list(color_data.get("personality", {}).keys())
personality = st.sidebar.selectbox("3. Select Personality:", personality_options)

# 4. Natural Lighting
lighting_options = list(color_data.get("natural lighting", {}).keys())
lighting = st.sidebar.selectbox("4. Select Natural Lighting Condition:", lighting_options)

# 5. Vastu Choice
vastu_choice_options = ["No", "Yes, strictly follow Vaastu", "Yes, but flexible"]
vastu_choice = st.sidebar.radio("5. Select Vaastu Choice:", vastu_choice_options)

# 6. Vastu Direction (Conditional - MODIFIED SECTION)
vastu_direction = None
vastu_direction_options = list(color_data.get("vaastu", {}).keys())
vastu_direction_options_display = ["Select from available options"] + [d.title() for d in vastu_direction_options]

if vastu_choice == "Yes, strictly follow Vaastu":
    # Point 2: Show message for strict vaastu compliance, direction inferred from lighting
    st.sidebar.markdown(
        "**Vaastu Direction:** Automatically **inferred from your Natural Lighting selection** for strict compliance."
    )
    # vastu_direction remains None, which triggers inference logic in recommendation functions.

elif vastu_choice == "Yes, but flexible":
    # Point 3: Show select box only for flexible vaastu
    selected_direction_display = st.sidebar.selectbox(
        "6. Select Vaastu Direction:", 
        vastu_direction_options_display
    )
    if selected_direction_display != "None (Infer from Lighting)":
        vastu_direction = selected_direction_display.lower()
# If vastu_choice is "No", nothing is displayed for section 6, which is correct.


# 7. Number of Colors
number_of_colors = st.sidebar.slider("6. Number of Colors to Recommend:", min_value=1, max_value=7, value=3)

# Button to trigger recommendations
submit_button = st.sidebar.button("Submit Your Preference")

# Main Content Area
if submit_button:
    
    # 1. Frequency Based Result
    st.header("1. Frequency Based Result 📊")
    st.markdown("*(Recommend colors based on frequency of occurrence)*")
    try:
        _, freq_result = get_recommendations_frequency(
            space=space, mood=mood, lighting=lighting, personality=personality, 
            vastu_choice=vastu_choice, vastu_direction=vastu_direction, 
            number_of_colors=number_of_colors
        )
        if freq_result:
            display_color_palette(freq_result, "freq")
        else:
            st.info("No colors found satisfying any criteria.")
    except Exception as e:
        st.error(f"Error in Frequency Based Result: {e}")
        
    st.markdown("---")

    # 2. Weighted Importance Based Result
    st.header("2. Weighted Importance Based Result ⚖️")
    st.markdown("*(Recommend colors based on predefined weights: Space(0.4) > Mood(0.25) > Lighting(0.15) > Personality(0.1) > Vaastu(0.1))*")
    try:
        _, weight_result = get_recommendations_weight(
            space=space, mood=mood, lighting=lighting, personality=personality, 
            vastu_choice=vastu_choice, vastu_direction=vastu_direction, 
            number_of_colors=number_of_colors
        )
        if weight_result:
            display_color_palette(weight_result, "weight")
        else:
            st.info("No colors found matching any criteria.")
    except Exception as e:
        st.error(f"Error in Weighted Importance Based Result: {e}")

    st.markdown("---")

    # 3. Rule Based Result
    st.header("3. Rule Based Result 📝")
    st.markdown("*(Recommend colors using Filter based Rule: Lighting → Space → Mood → Personality → Vaastu)*")
    try:
        _, rule_result = rule_based_recommendations(
            space=space, mood=mood, lighting=lighting, personality=personality, 
            vastu_choice=vastu_choice, vastu_direction=vastu_direction, 
            number_of_colors=number_of_colors
        )
        if rule_result:
            display_color_palette(rule_result, "rule")
        else:
            st.warning("No colors satisfy all sequential rules.")
    except Exception as e:
        st.error(f"Error in Rule Based Result: {e}")

    st.markdown("---")

    # 4. Constraint Based Result (Intersection)
    st.header("4. Constraint Based Result 🔒")
    st.markdown("*(Only colors that satisfy **ALL** user preferences simultaneously)*")
    try:
        _, constraint_result = constraint_satisfaction_recommendations(
            space=space, mood=mood, lighting=lighting, personality=personality, 
            vastu_choice=vastu_choice, vastu_direction=vastu_direction, 
            number_of_colors=number_of_colors
        )
        if constraint_result:
            display_color_palette(constraint_result, "constraint")
        else:
            st.warning("No color satisfies all constraints simultaneously.")
    except Exception as e:
        st.error(f"Error in Constraint Based Result: {e}")

    st.markdown("---")

    # 5. Multi-Criteria Decision Making (MCDM) Result
    st.header("5. Multi-Criteria Decision Making (MCDM) Result 🎯")
    st.markdown("*(Recommend colors based on the number of criteria they satisfy, all criteria equally weighted)*")
    try:
        _, mcdm_result = mcdm_color_recommendations(
            space=space, mood=mood, lighting=lighting, personality=personality, 
            vastu_choice=vastu_choice, vastu_direction=vastu_direction, 
            number_of_colors=number_of_colors
        )
        if mcdm_result:
            display_color_palette(mcdm_result, "mcdm")
        else:
            st.info("No colors found matching any criteria.")
    except Exception as e:
        st.error(f"Error in MCDM Result: {e}")

else:
    st.info("Please select your preferences in the sidebar and click **Submit Your Preference** to view the results.")
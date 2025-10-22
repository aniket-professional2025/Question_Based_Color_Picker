# # Importing Required Packages
# import streamlit as st
# from question_color_recommender import *

# # STREAMLIT UI
# st.set_page_config(page_title = "Color Recommendation System", layout = "wide")
# st.title("🎨 Berger Paint Recommendation System")

# # Initialize session state
# if "questions" not in st.session_state:
#     with st.spinner("Generating questions..."):
#         st.session_state.questions = generate_questions(palette)
#     st.session_state.answers = {}
#     st.session_state.q_idx = 0
#     st.session_state.recommendations = None

# # Setting the Questions as session states
# questions = st.session_state.questions
# q_idx = st.session_state.q_idx

# # Show current question
# if q_idx < len(questions):
#     q = questions[q_idx]
#     st.subheader(q["text"])
#     choice = st.radio("Select an option:", q["options"], key = q["id"])
#     st.session_state.answers[q["id"]] = choice

#     if st.button("Next"):
#         st.session_state.q_idx += 1
#         st.rerun()
# else:
#     # All questions answered
#     if st.session_state.recommendations is None:
#         with st.spinner("Getting your color recommendations..."):
#             st.session_state.recommendations = get_recommendations(
#                 palette, st.session_state.answers
#             )
#     # Getting the Recommendations
#     recs = st.session_state.recommendations
#     st.success("Here are your 5 recommended colors")

#     # Explanation on top
#     st.markdown(f"**Why these colors?**")
#     st.write(recs["explanation"])

#     # Colors displayed in a row
#     cols = st.columns(len(recs["colors"]))
#     for i, c in enumerate(recs["colors"]):
#         with cols[i]:
#             st.markdown(f"### {c['name']}")
#             st.markdown(f"**{c['hex']}**")
#             st.markdown(
#                 f"<div style='text-align:center; width:200px; height:120px; background:{c['hex']};"
#                 f"border-radius:12px;border:2px solid #333;margin-top:8px'></div>",
#                 unsafe_allow_html = True
#             )
    
#     # Add vertical space before button
#     st.markdown("<br><br>", unsafe_allow_html=True)

#     # The Start Over Button to Start the Complete Process Once Again
#     if st.button("Start Over"):
#         for key in ["questions", "answers", "q_idx", "recommendations"]:
#             st.session_state.pop(key, None)
#         st.rerun()


#################### NEW MODIFIED CODE #######################
# Importing Required Packages
import streamlit as st
from question_color_recommender import *

# STREAMLIT UI
st.set_page_config(page_title = "Color Recommendation System", layout = "wide")
st.title("🎨 Berger Paints Personalized Color Recommendation System")

# Initialize session state
if "started" not in st.session_state:
    st.session_state.started = False
if "questions" not in st.session_state:
    st.session_state.questions = None
    st.session_state.answers = {}
    st.session_state.q_idx = 0
    st.session_state.recommendations = None

# If not started, show start button
if not st.session_state.started:
    st.info("Click below to begin your personalized color recommendation journey.")
    if st.button("Start Your Journey"):
        with st.spinner("Generating questions..."):
            st.session_state.questions = generate_questions(palette)
        st.session_state.started = True
        st.rerun()

# If started, continue with the Q&A flow
elif st.session_state.questions:
    questions = st.session_state.questions
    q_idx = st.session_state.q_idx

    # Show current question
    if q_idx < len(questions):
        q = questions[q_idx]
        st.subheader(q["text"])
        choice = st.radio("Select an option:", q["options"], key = q["id"])
        st.session_state.answers[q["id"]] = choice

        if st.button("Next"):
            st.session_state.q_idx += 1
            st.rerun()
    else:
        # All questions answered
        if st.session_state.recommendations is None:
            with st.spinner("Getting your color recommendations..."):
                st.session_state.recommendations = get_recommendations(
                    palette, st.session_state.answers
                )

        # Getting the Recommendations
        recs = st.session_state.recommendations
        st.success("Here are your 3 recommended colors")

        # Explanation on top
        st.markdown("### How user selection guide the recommendation engine?")
        st.write(recs["analysis"])

        st.markdown(f"### Why these colors?")
        st.write(recs["explanation"])

        # Colors displayed in a row
        st.markdown("### The Recommended Colors are:")
        cols = st.columns(len(recs["colors"]))
        for i, c in enumerate(recs["colors"]):
            with cols[i]:
                st.markdown(f"### {c['name']}")
                st.markdown(f"**{c['hex']}**")
                st.markdown(
                    f"<div style='text-align:center; width:200px; height:120px; background:{c['hex']};"
                    f"border-radius:12px;border:2px solid #333;margin-top:8px'></div>",
                    unsafe_allow_html=True
                )

        # Add vertical space before button
        st.markdown("<br><br>", unsafe_allow_html=True)

        # The Start Over Button
        if st.button("Start Over"):
            for key in ["started", "questions", "answers", "q_idx", "recommendations"]:
                st.session_state.pop(key, None)
            st.rerun()
import streamlit as st
from services.groq_service import generate_project_idea


def render():
    st.markdown("#### 💡 Get a unique project idea")
    topic = st.text_input("Optional topic (e.g., 'sustainability', 'finance', 'game')",
                          placeholder="Leave blank for random idea")

    if st.button("Generate Idea", type="primary", use_container_width=True):
        with st.spinner("Brainstorming creative concepts..."):
            idea = generate_project_idea(topic if topic.strip() else None)

        if idea and idea.startswith("ERROR"):
            st.error(f"API Error: {idea}")
        elif idea:
            st.subheader("✨ Your Next Project")
            st.markdown(
                f'<div style="background:#0f172a; padding:1.5rem; border-radius:16px; font-size:1.1rem;">{idea}</div>',
                unsafe_allow_html=True)
        else:
            st.error("Idea generation failed.")
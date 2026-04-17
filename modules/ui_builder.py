import streamlit as st
from services.groq_service import build_ui_from_description
from utils.helpers import display_output_with_copy


def render():
    st.markdown("#### 🎨 Describe the UI component")
    description = st.text_area("UI description", height=150,
                               placeholder="Example: 'A modern login card with email, password, and a gradient button'")

    if st.button("Generate UI", type="primary", use_container_width=True):
        if not description.strip():
            st.warning("Please describe your UI requirement.")
        else:
            with st.spinner("Building UI components..."):
                ui_code, design_idea = build_ui_from_description(description)
            if ui_code:
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("📄 UI Code (HTML/CSS)")
                    display_output_with_copy(ui_code, "html")
                with col2:
                    st.subheader("🎯 Design Concept")
                    st.markdown(
                        f'<div style="background:#0f172a; padding:1rem; border-radius:16px;">{design_idea}</div>',
                        unsafe_allow_html=True)
            else:
                st.error("UI generation failed.")
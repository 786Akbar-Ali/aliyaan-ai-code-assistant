import streamlit as st
from services.groq_service import improve_code_quality
from utils.helpers import display_output_with_copy


def render():
    st.markdown("#### 🚀 Paste your code to enhance")
    code_input = st.text_area("Original code", height=250, placeholder="Python code for optimization...")

    if st.button("Improve Code", type="primary", use_container_width=True):
        if not code_input.strip():
            st.warning("Please provide code to improve.")
        else:
            with st.spinner("Enhancing code quality..."):
                improved, explanation = improve_code_quality(code_input)
            if improved:
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("✨ Improved Code")
                    display_output_with_copy(improved, "python")
                with col2:
                    st.subheader("📈 Improvements Explained")
                    st.markdown(
                        f'<div style="background:#0f172a; padding:1rem; border-radius:16px;">{explanation}</div>',
                        unsafe_allow_html=True)
            else:
                st.error("Improvement failed. Please try again.")
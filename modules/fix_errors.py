import streamlit as st
from services.groq_service import fix_code_errors
from utils.helpers import display_output_with_copy


def render():
    st.markdown("#### 🔧 Paste your buggy code below")
    code_input = st.text_area("Code with errors", height=250, placeholder="Paste Python code that needs fixing...")

    if st.button("Fix Errors", type="primary", use_container_width=True):
        if not code_input.strip():
            st.warning("Please enter some code.")
        else:
            with st.spinner("Analyzing and fixing errors..."):
                corrected, explanation = fix_code_errors(code_input)

            # Check for error from API
            if corrected and corrected.startswith("ERROR"):
                st.error(f"API Error: {corrected}")
            elif corrected:
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("✅ Corrected Code")
                    display_output_with_copy(corrected, "python")
                with col2:
                    st.subheader("📖 Explanation")
                    st.markdown(
                        f'<div style="background:#0f172a; padding:1rem; border-radius:16px;">{explanation}</div>',
                        unsafe_allow_html=True)
            else:
                st.error("Could not process the request. Please try again.")
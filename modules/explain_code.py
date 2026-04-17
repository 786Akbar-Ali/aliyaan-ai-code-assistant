import streamlit as st
from services.groq_service import explain_code_snippet
from utils.helpers import display_output_with_copy


def render():
    st.markdown("#### 📄 Paste code to understand")
    code_input = st.text_area("Code snippet", height=250, placeholder="Enter any code (Python, JS, etc.)")

    if st.button("Explain Code", type="primary", use_container_width=True):
        if not code_input.strip():
            st.warning("Please provide code to explain.")
        else:
            with st.spinner("Analyzing and explaining..."):
                explanation = explain_code_snippet(code_input)
            if explanation:
                st.subheader("🔍 Detailed Explanation")
                st.markdown(f'<div style="background:#0f172a; padding:1.5rem; border-radius:16px;">{explanation}</div>',
                            unsafe_allow_html=True)
            else:
                st.error("Explanation failed.")
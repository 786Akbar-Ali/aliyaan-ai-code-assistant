import streamlit as st
from services.groq_service import generate_code_from_prompt
from utils.helpers import display_output_with_copy


def render():
    st.markdown("#### ⚡ Describe the code you need")
    prompt = st.text_area("Natural language description", height=150,
                          placeholder="Example: 'Create a FastAPI endpoint that returns current weather data'")

    if st.button("Generate Code", type="primary", use_container_width=True):
        if not prompt.strip():
            st.warning("Please describe what code you want.")
        else:
            with st.spinner("Generating code..."):
                generated_code = generate_code_from_prompt(prompt)

            if generated_code and generated_code.startswith("ERROR"):
                st.error(f"API Error: {generated_code}")
            elif generated_code:
                st.subheader("💻 Generated Code")
                display_output_with_copy(generated_code, "python")
            else:
                st.error("Generation failed. No response from API.")
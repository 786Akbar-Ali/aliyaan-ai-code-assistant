import streamlit as st

def display_output_with_copy(code, language):
    """Display code block with copy button (built-in st.code copy)."""
    st.code(code, language=language, line_numbers=True)
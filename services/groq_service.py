import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path

from utils.prompts import (
    FIX_ERRORS_PROMPT, IMPROVE_CODE_PROMPT, GENERATE_CODE_PROMPT,
    UI_BUILDER_PROMPT, EXPLAIN_CODE_PROMPT, CREATE_IDEA_PROMPT,
    CONVERT_CODE_PROMPT
)

# =========================
# LOAD ENV (LOCAL SUPPORT)
# =========================
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# =========================
# GET API KEY (LOCAL + CLOUD)
# =========================
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY not found. Add it in .env (local) or Streamlit Secrets.")
    st.stop()

# =========================
# INIT CLIENT
# =========================
try:
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    st.error(f"❌ Failed to initialize Groq client: {e}")
    st.stop()

# =========================
# MODELS
# =========================
MODEL_CODE_GEN = "llama-3.3-70b-versatile"
MODEL_FIX_IMPROVE = "llama-3.3-70b-versatile"
MODEL_EXPLAIN_IDEA = "llama-3.1-8b-instant"

# =========================
# CORE FUNCTION
# =========================
def call_groq(model, messages, temperature=0.3):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=2048
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"ERROR: {str(e)}"

# =========================
# FEATURES
# =========================
def fix_code_errors(code):
    messages = [
        {"role": "system", "content": FIX_ERRORS_PROMPT},
        {"role": "user", "content": f"Fix errors in this code:\n{code}"}
    ]
    result = call_groq(MODEL_FIX_IMPROVE, messages)

    if result and not result.startswith("ERROR"):
        if "###" in result:
            corrected, explanation = result.split("###", 1)
            return corrected.strip(), explanation.strip()
        return result, "Correction applied."

    return result, None


def improve_code_quality(code):
    messages = [
        {"role": "system", "content": IMPROVE_CODE_PROMPT},
        {"role": "user", "content": f"Improve this code:\n{code}"}
    ]
    result = call_groq(MODEL_FIX_IMPROVE, messages)

    if result and not result.startswith("ERROR"):
        if "###" in result:
            improved, explanation = result.split("###", 1)
            return improved.strip(), explanation.strip()
        return result, "Code optimized."

    return result, None


def generate_code_from_prompt(prompt):
    messages = [
        {"role": "system", "content": GENERATE_CODE_PROMPT},
        {"role": "user", "content": prompt}
    ]
    return call_groq(MODEL_CODE_GEN, messages)


def build_ui_from_description(desc):
    messages = [
        {"role": "system", "content": UI_BUILDER_PROMPT},
        {"role": "user", "content": desc}
    ]
    result = call_groq(MODEL_CODE_GEN, messages)

    if result and not result.startswith("ERROR"):
        if "###" in result:
            ui_code, design = result.split("###", 1)
            return ui_code.strip(), design.strip()
        return result, "Modern UI design with glassmorphism."

    return None, None


def explain_code_snippet(code):
    messages = [
        {"role": "system", "content": EXPLAIN_CODE_PROMPT},
        {"role": "user", "content": f"Explain this code:\n{code}"}
    ]
    return call_groq(MODEL_EXPLAIN_IDEA, messages)


def generate_project_idea(topic=None):
    user_msg = (
        f"Generate a unique project idea about: {topic}"
        if topic else
        "Generate a random creative project idea."
    )

    messages = [
        {"role": "system", "content": CREATE_IDEA_PROMPT},
        {"role": "user", "content": user_msg}
    ]
    return call_groq(MODEL_EXPLAIN_IDEA, messages)


def convert_code(source_code, source_lang, target_lang):
    prompt = CONVERT_CODE_PROMPT.format(
        source_lang=source_lang,
        target_lang=target_lang,
        code=source_code
    )

    messages = [
        {"role": "system", "content": "You are a code conversion expert."},
        {"role": "user", "content": prompt}
    ]

    result = call_groq(MODEL_CODE_GEN, messages)

    if result and not result.startswith("ERROR"):
        return result

    return "Conversion failed."

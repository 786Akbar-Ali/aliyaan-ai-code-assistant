import streamlit as st
from datetime import datetime
from modules import (
    fix_errors,
    improve_code,
    generate_code,
    ui_builder,
    explain_code,
    create_idea,
)
from services.groq_service import convert_code

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Aliyaan AI Code Assistant | by Akbar Ali",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- SESSION STATE ----------
if "selected_module" not in st.session_state:
    st.session_state.selected_module = None
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "history" not in st.session_state:
    st.session_state.history = []
if "language" not in st.session_state:
    st.session_state.language = "Python"
if "show_history" not in st.session_state:
    st.session_state.show_history = False
if "last_input" not in st.session_state:
    st.session_state.last_input = ""
if "last_output" not in st.session_state:
    st.session_state.last_output = ""

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .main .block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 1400px; }
    .glass-card {
        border-radius: 28px; padding: 1.8rem 1rem; text-align: center;
        transition: all 0.3s cubic-bezier(0.2, 0.9, 0.4, 1.1);
        margin-bottom: 1.2rem; cursor: pointer;
    }
    .glass-card:hover {
        transform: translateY(-5px) scale(1.02);
        border-color: #818cf8;
        box-shadow: 0 0 25px rgba(96, 165, 250, 0.5);
        background: rgba(30, 45, 80, 0.7);
    }
    .card-icon { font-size: 3rem; margin-bottom: 1rem; }
    .card-title { font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
    .card-desc { font-size: 0.9rem; color: #94a3b8; }
    .hero-title { font-size: 3.8rem; font-weight: 800; text-align: center; margin-bottom: 0.2rem; letter-spacing: -0.02em; }
    .hero-subtitle { text-align: center; color: #94a3b8; font-size: 1.2rem; margin-bottom: 1rem; }
    .footer { text-align: center; color: #64748b; font-size: 0.8rem; margin-top: 3rem; padding: 1rem; border-top: 1px solid rgba(96, 165, 250, 0.2); }
    .top-bar { display: flex; justify-content: flex-end; align-items: center; gap: 1rem; padding: 0.5rem 1rem; margin-bottom: 1rem; }
    .stCodeBlock { border-radius: 16px; }
    .history-item { background: rgba(20, 30, 55, 0.4); border-radius: 16px; padding: 0.8rem; margin-bottom: 0.8rem; }
</style>
""", unsafe_allow_html=True)


def apply_theme():
    if st.session_state.dark_mode:
        st.markdown("""
        <style>
            .stApp { background: linear-gradient(135deg, #0a0f2a 0%, #030614 50%, #0a0f2a 100%); background-size: 200% 200%; animation: gradientShift 12s ease infinite; }
            @keyframes gradientShift { 0% { background-position: 0% 0%; } 50% { background-position: 100% 100%; } 100% { background-position: 0% 0%; } }
            .glass-card { background: rgba(20, 30, 55, 0.5); backdrop-filter: blur(12px); border: 1px solid rgba(96, 165, 250, 0.3); }
            .card-title { color: #e2e8f0; }
            .hero-title { background: linear-gradient(135deg, #c084fc, #60a5fa, #38bdf8); -webkit-background-clip: text; background-clip: text; color: transparent; }
            .stButton > button { background: rgba(30, 45, 80, 0.7); color: white; }
            .stTextArea textarea, .stTextInput input { background: #0f172a; color: #f1f5f9; }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            .stApp { background: linear-gradient(135deg, #f0f4ff 0%, #e0e8ff 100%); }
            .glass-card { background: rgba(255,255,255,0.6); backdrop-filter: blur(8px); border: 1px solid rgba(0,0,0,0.1); }
            .card-title { color: #1e293b; }
            .hero-title { background: linear-gradient(135deg, #4f46e5, #0ea5e9); -webkit-background-clip: text; background-clip: text; color: transparent; }
            .stButton > button { background: rgba(100,116,139,0.2); color: #1e293b; }
        </style>
        """, unsafe_allow_html=True)


def add_to_history(module_name, input_text, output_text):
    st.session_state.history.insert(0, {
        "module": module_name,
        "input": input_text[:150] + "..." if len(input_text) > 150 else input_text,
        "output": output_text[:300] + "..." if len(output_text) > 300 else output_text,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    st.session_state.history = st.session_state.history[:15]


def clear_history():
    st.session_state.history = []
    st.toast("History cleared!", icon="🗑️")


def top_bar():
    col1, col2, col3 = st.columns([6, 1, 1])
    with col2:
        if st.button("📜 History", help="View recent outputs"):
            st.session_state.show_history = not st.session_state.show_history
            st.rerun()
    with col3:
        if st.button("🌓" if st.session_state.dark_mode else "☀️", help="Toggle Dark Mode"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()


# ---------- DASHBOARD ----------
def show_dashboard():
    apply_theme()
    top_bar()
    st.markdown('<div class="hero-title">⚡ Aliyaan AI Code Assistant</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">by Akbar Ali · Intelligent coding companion · Generate · Fix · Explain · Create</div>',
        unsafe_allow_html=True)

    col_lang, _ = st.columns([1, 3])
    with col_lang:
        st.session_state.language = st.selectbox("🌐 Default language for generation",
                                                 ["Python", "JavaScript", "Java", "C++"], index=0)

    modules_data = [
        {"name": "Fix Errors", "icon": "🛠", "desc": "Detect & resolve bugs instantly", "key": "fix_errors"},
        {"name": "Improve Code", "icon": "🚀", "desc": "Optimize performance & style", "key": "improve_code"},
        {"name": "Generate Code", "icon": "⚡", "desc": "Build from natural language", "key": "generate_code"},
        {"name": "UI Builder", "icon": "🎨", "desc": "Generate HTML/CSS components", "key": "ui_builder"},
        {"name": "Explain Code", "icon": "📘", "desc": "Deep understanding of logic", "key": "explain_code"},
        {"name": "Create Idea", "icon": "💡", "desc": "Innovative project concepts", "key": "create_idea"},
    ]

    cols = st.columns(3)
    for idx, mod in enumerate(modules_data):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="glass-card">
                <div class="card-icon">{mod['icon']}</div>
                <div class="card-title">{mod['name']}</div>
                <div class="card-desc">{mod['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Open {mod['name']}", key=f"btn_{mod['key']}", use_container_width=True):
                st.session_state.selected_module = mod["key"]
                st.rerun()

    with st.expander("🔄 Advanced: Python ↔ JavaScript Converter", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            source_lang = st.selectbox("From language", ["Python", "JavaScript"], key="conv_from")
            source_code = st.text_area("Source code", height=200, placeholder="Paste your code here...")
        with col2:
            target_lang = "JavaScript" if source_lang == "Python" else "Python"
            st.markdown(f"**To {target_lang}**")
            if st.button("Convert Code", type="primary"):
                if source_code.strip():
                    with st.spinner("Converting..."):
                        converted = convert_code(source_code, source_lang.lower(), target_lang.lower())
                        if converted and "ERROR" not in converted:
                            st.code(converted, language=target_lang.lower())
                            st.toast("✅ Conversion complete!", icon="🎉")
                            # Save to history manually via button
                            st.session_state.last_input = source_code
                            st.session_state.last_output = converted
                            if st.button("💾 Save this conversion to history", key="save_conv"):
                                add_to_history("Code Converter", source_code, converted)
                                st.toast("Saved to history!", icon="📁")
                        else:
                            st.error(converted)
                else:
                    st.warning("Please enter source code.")
        st.caption("Powered by Groq AI — intelligent syntax transformation.")

    if st.session_state.show_history:
        with st.expander("📜 Recent History", expanded=True):
            if not st.session_state.history:
                st.info("No history yet. After using a module, click 'Save to History' below the output.")
            else:
                for entry in st.session_state.history:
                    st.markdown(f"**{entry['module']}** – *{entry['timestamp']}*")
                    st.caption(f"Input: {entry['input']}")
                    st.caption(f"Output: {entry['output']}")
                    st.markdown("---")
                if st.button("Clear History", key="clear_hist"):
                    clear_history()
                    st.rerun()

    st.markdown('<div class="footer">Developed with ❤️ by Akbar Ali | Aliyaan AI Code Assistant</div>',
                unsafe_allow_html=True)


# ---------- MODULE RENDERER WITH MANUAL HISTORY SAVE ----------
def render_module(module_name):
    apply_theme()
    top_bar()

    col1, col2 = st.columns([1, 10])
    with col1:
        if st.button("← Back", key="back_btn", help="Return to dashboard"):
            st.session_state.selected_module = None
            st.rerun()
    with col2:
        st.markdown(f"## {module_name.replace('_', ' ').title()}")

    # Call the original module
    if module_name == "fix_errors":
        fix_errors.render()
    elif module_name == "improve_code":
        improve_code.render()
    elif module_name == "generate_code":
        generate_code.render()
    elif module_name == "ui_builder":
        ui_builder.render()
    elif module_name == "explain_code":
        explain_code.render()
    elif module_name == "create_idea":
        create_idea.render()

    # After module, provide a way to save to history (manual)
    # The user can copy the output from the screen and click save.
    # For better UX, we ask for input and output.
    with st.expander("💾 Save this result to History", expanded=False):
        col_a, col_b = st.columns(2)
        with col_a:
            input_text = st.text_area("Input (prompt/code)", placeholder="Paste what you entered", key="hist_input")
        with col_b:
            output_text = st.text_area("Output (result)", placeholder="Paste the AI response", key="hist_output")
        if st.button("Save to History", key="save_hist"):
            if input_text and output_text:
                add_to_history(module_name.replace('_', ' ').title(), input_text, output_text)
                st.toast("Saved to history!", icon="✅")
                st.rerun()
            else:
                st.warning("Please fill both input and output fields.")

    st.markdown('<div class="footer">Developed with ❤️ by Akbar Ali | Aliyaan AI Code Assistant(17/04/2026</div>',
                unsafe_allow_html=True)


# ---------- MAIN ----------
if st.session_state.selected_module is None:
    show_dashboard()
else:
    render_module(st.session_state.selected_module)
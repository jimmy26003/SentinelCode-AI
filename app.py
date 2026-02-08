import streamlit as st
import time
from scanner_engine import run_security_scan as scan_file

# --- Page Configuration ---
st.set_page_config(
    page_title="SentinelCode AI | Security Hub",
    page_icon="🛡️",
    layout="centered"
)

# --- Custom CSS Styling ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background: linear-gradient(45deg, #ff4b4b, #ff8f8f);
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header Section ---
st.image("https://cdn-icons-png.flaticon.com/512/1053/1053210.png", width=80)
st.title("🛡️ SentinelCode AI")
st.markdown("#### Next-Generation Vulnerability Scanner")
st.write("---")

# --- File Upload Section ---
uploaded_file = st.file_uploader("Upload Python file (.py) for deep analysis", type=['py'])

if uploaded_file is not None:
    # Processing Animation
    with st.status("🔍 Analyzing code structure...", expanded=True) as status:
        st.write("Parsing Abstract Syntax Tree (AST)...")
        time.sleep(1)
        st.write("Scanning for security patterns...")
        time.sleep(1)
        
        # Calling your engine
        results = scan_file(uploaded_file) 
        
        status.update(label="✅ Analysis Complete!", state="complete", expanded=False)

    # --- Results Display ---
    st.write("### 📊 Security Report")
    
    if not results:
        st.balloons()
        st.success("Clean Scan! No critical vulnerabilities detected.")
    else:
        for error in results:
            with st.expander(f"⚠️ Issue: {error.get('type', 'Vulnerability Detected')}"):
                st.error(f"**Description:** {error.get('description')}")
                st.code(error.get('code_snippet'), language='python')
                st.info(f"**Recommendation:** {error.get('recommendation')}")

# --- Footer ---
st.write("---")
st.caption("Developed by SentinelCode AI Team © 2026")
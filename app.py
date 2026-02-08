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
    with st.status("🔍 Analyzing code structure...", expanded=True) as status:
        st.write("Parsing Abstract Syntax Tree (AST)...")
        time.sleep(1)
        st.write("Scanning for security patterns...")
        time.sleep(1)
        
        results = scan_file(uploaded_file) 
        
        status.update(label="✅ Analysis Complete!", state="complete", expanded=False)

    st.write("### 📊 Security Report")
    
    if not results or (isinstance(results, dict) and not results.get('results')):
        st.balloons()
        st.success("Clean Scan! No critical vulnerabilities detected.")
    else:
        # Handling Bandit JSON output structure
        issues = results.get('results', []) if isinstance(results, dict) else results
        for error in issues:
            with st.expander(f"⚠️ Issue: {error.get('test_name', 'Vulnerability')}"):
                st.error(f"**Severity:** {error.get('issue_severity')}")
                st.write(f"**Description:** {error.get('issue_text')}")
                st.code(error.get('code'), language='python')
                st.info(f"**Line:** {error.get('line_number')}")

# --- Professional Footer ---
st.write("---")
f_col1, f_col2, f_col3 = st.columns(3)
with f_col1:
    st.caption("🔒 Secure Analysis")
with f_col2:
    st.caption("⚡ Powered by Bandit")
with f_col3:
    st.caption("🛠️ Version 1.0.1")

st.markdown(
    "<div style='text-align: center; color: grey; font-size: 0.8em;'>Developed by SentinelCode AI Team © 2026</div>", 
    unsafe_allow_html=True
)
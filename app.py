import streamlit as st
import time
import tempfile
import os
from scanner_engine import run_security_scan as scan_file

st.set_page_config(
    page_title="SentinelCode AI | Security Hub",
    page_icon="🛡️",
    layout="centered"
)

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background: linear-gradient(45deg, #ff4b4b, #ff8f8f);
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ SentinelCode AI")
st.markdown("#### Next-Generation Vulnerability Scanner")
st.write("---")

uploaded_file = st.file_uploader("Upload Python file (.py) for deep analysis", type=['py'])

if uploaded_file is not None:
    with st.status("🔍 Analyzing code structure...", expanded=True) as status:
        # Create a temporary file to scan
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        results = scan_file(tmp_path)
        os.unlink(tmp_path) # Clean up
        status.update(label="✅ Analysis Complete!", state="complete", expanded=False)

    st.write("### 📊 Security Report")
    
    # Process Bandit Results
    issues = results.get('results', [])
    if not issues:
        st.balloons()
        st.success("Clean Scan! No critical vulnerabilities detected.")
    else:
        st.warning(f"Found {len(issues)} potential security issues")
        for error in issues:
            severity = error.get('issue_severity', 'UNDEFINED')
            color = "#ff4b4b" if severity == "HIGH" else "#ffa500"
            
            with st.expander(f"⚠️ {error.get('test_name')} - {severity} SEVERITY"):
                st.markdown(f"<span style='color:{color}'>**Description:**</span> {error.get('issue_text')}", unsafe_allow_html=True)
                st.code(error.get('code'), language='python')
                st.info(f"Line: {error.get('line_number')} | Confidence: {error.get('issue_confidence')}")

st.write("---")
f_col1, f_col2, f_col3 = st.columns(3)
with f_col1: st.caption("🔒 Secure Analysis")
with f_col2: st.caption("⚡ Powered by Bandit")
with f_col3: st.caption("🛠️ Version 1.0.1")
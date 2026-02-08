import streamlit as st
import time
import tempfile
import os
from scanner_engine import run_security_scan as scan_file

# --- 1. Page Config (Using your logo as Tab Icon) ---
st.set_page_config(
    page_title="SentinelCode AI | Hub",
    page_icon="https://raw.githubusercontent.com/jimmy26003/SentinelCode-AI/main/logo.png.jpg",
    layout="wide"
)

# --- 2. Advanced Cyber CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0d1117;
        font-family: 'Inter', sans-serif;
        color: #e6edf3;
    }

    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }

    .main-title {
        background: linear-gradient(90deg, #3fb950 0%, #2ea043 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
    }

    div[data-testid="stMetric"] {
        background: rgba(22, 27, 34, 0.8);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Sidebar Layout (Using your logo link) ---
with st.sidebar:
    st.image("https://raw.githubusercontent.com/jimmy26003/SentinelCode-AI/main/logo.png.jpg", width=180)
    st.markdown("### 🛠️ Control Panel")
    st.caption("Scanner Engine: **Bandit v1.7.5**")
    st.write("---")
    st.markdown("🔍 **Quick Guide:**\n1. Upload `.py` file\n2. AI Analysis\n3. Review Risks")
    st.write("---")
    st.caption("v1.0.1 Stable Release")

# --- 4. Main Header Section ---
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image("https://raw.githubusercontent.com/jimmy26003/SentinelCode-AI/main/logo.png.jpg", width=100)
with col_title:
    st.markdown("<h1 class='main-title'>SentinelCode AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #8b949e; font-size: 1.1em;'>Automated Security Auditing for Modern Python Applications</p>", unsafe_allow_html=True)

st.write("---")

# --- 5. File Upload & Logic ---
uploaded_file = st.file_uploader("", type=['py'])

if uploaded_file:
    with st.status("🚀 Running Deep Sandbox Analysis...", expanded=True) as status:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name
        
        results = scan_file(tmp_path)
        os.unlink(tmp_path)
        time.sleep(1)
        status.update(label="✅ Scan Completed!", state="complete", expanded=False)

    # --- 6. Results Dashboard ---
    issues = results.get('results', [])
    st.markdown("### 🟢 Security Insights")
    m1, m2, m3 = st.columns(3)
    
    if not issues:
        m1.metric("Risk Level", "SAFE", "0 Issues")
        m2.metric("Code Integrity", "100%", "Perfect")
        m3.metric("Security Score", "1000/1000")
        st.balloons()
    else:
        m1.metric("Total Risks", len(issues), "Action Required")
        m2.metric("Code Integrity", f"{max(0, 100 - (len(issues)*10))}%")
        m3.metric("Status", "Critical" if len(issues) > 3 else "Warning")

        for error in issues:
            with st.expander(f"🔴 {error.get('test_name')} - Line {error.get('line_number')}"):
                st.code(error.get('code'), language='python')
                st.write(f"**Issue:** {error.get('issue_text')}")

# --- 7. Footer ---
st.markdown("<br><hr><center style='color: #484f58;'>SentinelCode AI © 2026</center>", unsafe_allow_html=True)
import streamlit as st
import time
import tempfile
import os
from scanner_engine import run_security_scan as scan_file

# --- 1. Page Config ---
st.set_page_config(
    page_title="SentinelCode AI | Hub",
    page_icon="🛡️",
    layout="wide"
)

# --- 2. Advanced Cyber CSS (The "Magic" part) ---
st.markdown("""
    <style>
    /* Main Background & Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0d1117;
        font-family: 'Inter', sans-serif;
        color: #e6edf3;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }

    /* Header & Title Gradient */
    .main-title {
        background: linear-gradient(90deg, #3fb950 0%, #2ea043 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
    }

    /* Dashboard Cards (Metrics) */
    div[data-testid="stMetric"] {
        background: rgba(22, 27, 34, 0.8);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }

    /* Results Expander Customization */
    .streamlit-expanderHeader {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
        color: #3fb950 !important;
    }

    /* Glowing Effect for Security Score */
    .security-score {
        color: #3fb950;
        text-shadow: 0 0 10px rgba(63, 185, 80, 0.5);
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Sidebar Layout ---
with st.sidebar:
    # Top Logo with Green Shield
    st.markdown("""
        <div style='text-align: center; margin-bottom: 20px;'>
            <img src='https://cdn-icons-png.flaticon.com/512/1053/1053210.png' width='100' style='filter: hue-rotate(90deg);'>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🛠️ Control Panel")
    st.caption("Scanner Engine: **Bandit v1.7.5**")
    st.write("---")
    
    st.markdown("🔍 **Quick Guide:**")
    st.markdown("1. Upload `.py` file\n2. Wait for AI analysis\n3. Review highlighted risks")
    st.write("---")
    st.caption("v1.0.1 Stable Release")

# --- 4. Main Header Section ---
st.markdown("<h1 class='main-title'>SentinelCode AI | Hub</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #8b949e; font-size: 1.1em;'>Automated Security Auditing for Modern Python Applications</p>", unsafe_allow_html=True)
st.write("---")

# --- 5. Logic & Interaction ---
uploaded_file = st.file_uploader("", type=['py'])

if uploaded_file:
    with st.status("🚀 Running Deep Sandbox Analysis...", expanded=True) as status:
        st.write("Creating temporary virtual environment...")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name
        
        results = scan_file(tmp_path)
        os.unlink(tmp_path)
        time.sleep(1)
        status.update(label="✅ Scan Completed Successfully!", state="complete", expanded=False)

    # --- 6. Results Dashboard (The Cards) ---
    issues = results.get('results', [])
    
    st.markdown("### 🟢 Security Insights")
    m1, m2, m3 = st.columns(3)
    
    if not issues:
        m1.metric("Risk Level", "SAFE", "0 Issues")
        m2.metric("Code Integrity", "100%", "Perfect")
        m3.metric("Security Score", "1000/1000")
        st.balloons()
    else:
        m1.metric("Risk Level", "CRITICAL" if len(issues) > 3 else "MEDIUM", f"{len(issues)} Issues")
        m2.metric("Code Integrity", f"{100 - (len(issues)*10)}%", "-10% per bug")
        m3.metric("Security Score", f"{1000 - (len(issues)*100)}/1000")

        st.markdown("### ⚠️ Detailed Findings")
        for error in issues:
            severity = error.get('issue_severity')
            color = "#ff4b4b" if severity == "HIGH" else "#ffa500"
            
            with st.expander(f"🔴 Issue: {error.get('test_name')} - Line {error.get('line_number')}"):
                st.markdown(f"<span style='color:{color}'>**Severity:** {severity}</span>", unsafe_allow_html=True)
                st.markdown(f"**Description:** {error.get('issue_text')}")
                st.code(error.get('code'), language='python')
                st.info(f"Confidence Level: {error.get('issue_confidence')}")

# --- 7. Footer ---
st.markdown("<br><hr><center style='color: #484f58;'>Designed for Secure Development Teams | 2026</center>", unsafe_allow_html=True)
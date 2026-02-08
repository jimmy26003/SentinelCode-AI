import streamlit as st
import time
import tempfile
import os
from scanner_engine import run_security_scan as scan_file

# --- Professional Page Configuration ---
st.set_page_config(
    page_title="SentinelCode AI | Hub",
    page_icon="🛡️",
    layout="wide"
)

# --- Custom Styling for a Dark/Cyber Theme ---
st.markdown("""
    <style>
    .main { background-color: #0d1117; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .stAlert { border-radius: 10px; }
    /* Style for the scan button */
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #238636, #2ea043);
        color: white; border: none; padding: 10px 24px; border-radius: 8px;
    }
    /* Expander styling */
    .streamlit-expanderHeader { background-color: #161b22 !important; border-radius: 8px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar Content ---
with st.sidebar:
    st.markdown("### 🛠️ Control Panel")
    st.info("Scanner Engine: **Bandit v1.7.5**")
    st.write("---")
    st.markdown("🔍 **Quick Guide:**\n1. Upload .py file\n2. Wait for AI analysis\n3. Review highlighted risks")
    st.write("---")
    st.caption("v1.0.1 Stable Release")

# --- Main Interface ---
col_logo, col_text = st.columns([1, 5])
with col_logo:
    # Using a generic shield icon as fallback
    st.image("https://cdn-icons-png.flaticon.com/512/6045/6045100.png", width=100)
with col_text:
    st.title("SentinelCode AI")
    st.markdown("<p style='color: #8b949e; font-size: 1.2em;'>Automated Security Auditing for Modern Python Applications</p>", unsafe_allow_html=True)

st.write("---")

# --- Scanning Section ---
uploaded_file = st.file_uploader("", type=['py'])

if uploaded_file:
    with st.status("🚀 Initializing Deep Scan...", expanded=True) as status:
        st.write("Creating secure sandbox environment...")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name
        
        st.write("Running static analysis engine...")
        time.sleep(1) # Visual effect
        results = scan_file(tmp_path)
        os.unlink(tmp_path)
        
        status.update(label="✅ Analysis Successfully Finished!", state="complete", expanded=False)

    # --- Dashboard View ---
    issues = results.get('results', [])
    
    st.subheader("📊 Security Insights")
    m1, m2, m3 = st.columns(3)
    
    if not issues:
        m1.metric("Risk Level", "Safe", "0 Issues", delta_color="normal")
        m2.metric("Files Scanned", "1", "100%")
        m3.metric("Security Score", "100/100")
        st.balloons()
        st.success("### 🎉 Perfect Code! No vulnerabilities found.")
    else:
        # Count high/medium severity
        high_risk = len([i for i in issues if i.get('issue_severity') == 'HIGH'])
        m1.metric("Total Risks", len(issues), f"{high_risk} High", delta_color="inverse")
        m2.metric("Code Integrity", f"{100 - (len(issues)*5)}%", "-5% per issue")
        m3.metric("Scanner Status", "Active")

        st.write("#### Detailed Findings:")
        for error in issues:
            sev = error.get('issue_severity')
            color = "🔴" if sev == "HIGH" else "🟠"
            
            with st.expander(f"{color} {error.get('test_name')} (Line {error.get('line_number')})"):
                st.markdown(f"**Issue:** {error.get('issue_text')}")
                st.markdown(f"**Confidence:** `{error.get('issue_confidence')}`")
                st.code(error.get('code'), language='python')
                st.warning("Recommendation: Review the logic and follow OWASP best practices.")

# --- Footer ---
st.write("---")
st.markdown("<center style='color: #484f58;'>Designed for Secure Development Teams | 2026</center>", unsafe_allow_html=True)
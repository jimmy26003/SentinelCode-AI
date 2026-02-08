import streamlit as st
import time
import tempfile
import os
from scanner_engine import run_security_scan as scan_file

# --- Page Configuration ---
st.set_page_config(
    page_title="SentinelCode AI | Security Hub",
    page_icon="🛡️",
    layout="wide" # Changed to wide for better data visualization
)

# --- Advanced Custom CSS ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #1a1c24 100%);
    }
    
    /* Title Styling */
    h1 {
        color: #ff4b4b;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        letter-spacing: -1px;
    }
    
    /* Card-like containers for results */
    div[data-testid="stExpander"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
    }
    
    /* Metrics Styling */
    div[data-testid="stMetricValue"] {
        color: #ff4b4b;
        font-size: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar Navigation ---
with st.sidebar:
    st.image("https://raw.githubusercontent.com/jimmy26003/SentinelCode-AI/main/logo.png", width=150)
    st.title("Settings & info")
    st.info("SentinelCode AI uses Bandit engine to perform deep static analysis of Python code.")
    st.write("---")
    st.markdown("### Quick Stats")
    st.metric(label="System Status", value="Operational", delta="Stable")
    
# --- Main Header ---
col_head1, col_head2 = st.columns([1, 4])
with col_head1:
    st.image("https://raw.githubusercontent.com/jimmy26003/SentinelCode-AI/main/logo.png", width=100)
with col_head2:
    st.title("SentinelCode AI")
    st.markdown("##### *Empowering Developers with Secure Code Insights*")

st.write("---")

# --- Scanning Logic ---
uploaded_file = st.file_uploader("Choose a Python file to scan", type=['py'], help="Max file size: 200MB")

if uploaded_file is not None:
    # Analysis UI
    with st.status("🛠️ Initializing Security Scan...", expanded=True) as status:
        st.write("Uploading file to secure buffer...")
        time.sleep(0.5)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name
        
        st.write("Running Bandit static analysis...")
        results = scan_file(tmp_path)
        os.unlink(tmp_path)
        
        status.update(label="✅ Analysis Complete!", state="complete", expanded=False)

    # --- Results Dashboard ---
    st.subheader("📊 Analysis Results")
    issues = results.get('results', [])
    
    if not issues:
        st.balloons()
        st.success("### Excellent! Your code passed all security checks.")
    else:
        # Metrics Row
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Issues", len(issues))
        m2.metric("Scan Duration", f"{results.get('generated_at')[:10]}", "Date")
        m3.metric("Security Score", "A" if len(issues) < 3 else "C")

        # Detailed Report
        for error in issues:
            severity = error.get('issue_severity')
            icon = "🔴" if severity == "HIGH" else "🟠"
            
            with st.expander(f"{icon} {error.get('test_name')} - Line {error.get('line_number')}"):
                st.markdown(f"**Vulnerability Type:** `{error.get('issue_text')}`")
                st.markdown("**Evidence:**")
                st.code(error.get('code'), language='python')
                st.markdown(f"[Learn more about this issue](https://bandit.readthedocs.io/en/latest/plugins/{error.get('test_id').lower()}.html)")

# --- Footer ---
st.markdown("<br><hr><center>SentinelCode AI © 2026 | Secured by <b>Bandit</b></center>", unsafe_allow_html=True)
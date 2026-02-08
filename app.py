import streamlit as st
import requests

st.title("🛡️ SentinelCode AI")
st.write("Upload your code to check for security vulnerabilities")

uploaded_file = st.file_uploader("Choose a Python file", type="py")

if uploaded_file is not None:
    if st.button("Analyze Code"):
        # Sending file to your running FastAPI server
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        response = requests.post("http://127.0.0.1:8000/scan", files=files)
        
        if response.status_code == 200:
            result = response.json()
            st.success("Analysis Complete!")
            st.json(result) # This will display the vulnerabilities found
        else:
            st.error("Backend server is not responding. Make sure main.py is running.")
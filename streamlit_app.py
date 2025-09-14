import streamlit as st
import pandas as pd
import io
import json
from brutalyze_core import analyze_log

st.set_page_config(
    page_title="🛡️ Brutalyze Web",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Brutalyze Web")
st.markdown("**Privacy-focused SSH log analysis tool**")

# Sidebar for file upload and options
with st.sidebar:
    st.header("📁 Upload Options")
    
    # File upload or sample option
    use_sample = st.checkbox("Use Sample Log File", help="Use the included sample auth.log file")
    
    if not use_sample:
        uploaded_file = st.file_uploader(
            "Upload Log File (.log)", 
            type=['log', 'txt'],
            help="Upload your SSH auth.log file for analysis"
        )
    else:
        uploaded_file = None
    
    st.header("⚙️ Analysis Options")
    threshold = st.number_input(
        "Brute-force Threshold", 
        min_value=1, 
        value=3, 
        help="Minimum failed attempts to flag as brute-force"
    )
    
    window = st.number_input(
        "Time Window (minutes)", 
        min_value=1, 
        value=1, 
        help="Time window for brute-force detection"
    )

# Main content area
if st.button("🔍 Analyze Logs", type="primary"):
    if use_sample:
        log_path = "sample_auth.log"
        st.success("Using sample log file")
    elif uploaded_file is not None:
        # Save uploaded file temporarily
        with open("temp_upload.log", "wb") as f:
            f.write(uploaded_file.getbuffer())
        log_path = "temp_upload.log"
        st.success(f"Uploaded: {uploaded_file.name}")
    else:
        st.error("Please upload a log file or use the sample file")
        st.stop()
    
    # Show progress
    with st.spinner("Analyzing logs..."):
        result = analyze_log(log_path)
    
    # Display summary
    st.header("📊 Analysis Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🔴 Failed Logins", 
            value=result["summary"]["failed_logins"]
        )
    
    with col2:
        st.metric(
            label="🟢 Successful Logins", 
            value=result["summary"]["successful_logins"]
        )
    
    with col3:
        st.metric(
            label="⚠️ Suspicious", 
            value=result["summary"]["suspicious"]
        )
    
    with col4:
        st.metric(
            label="📄 Other", 
            value=result["summary"]["other"]
        )
    
    # Display alerts
    if result["alerts"]:
        st.header("🚨 Security Alerts")
        for alert in result["alerts"]:
            st.error(alert)
    
    # Download buttons
    st.header("📥 Download Reports")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # CSV Download
        csv_data = []
        csv_data.append(["Timestamp", "User", "IP", "Country", "Region", "City", "Category", "Raw Log"])
        
        for category, logs in result["classified"].items():
            for log in logs:
                loc = log.get("location", {})
                csv_data.append([
                    log.get("timestamp", ""),
                    log.get("user", ""),
                    log.get("ip", ""),
                    loc.get("country", ""),
                    loc.get("region", ""),
                    loc.get("city", ""),
                    category,
                    log.get("raw", "")
                ])
        
        df = pd.DataFrame(csv_data[1:], columns=csv_data[0])
        csv = df.to_csv(index=False)
        
        st.download_button(
            label="📊 Download CSV",
            data=csv,
            file_name="brutalyze_report.csv",
            mime="text/csv"
        )
    
    with col2:
        # JSON Download
        json_data = json.dumps(result, indent=4)
        st.download_button(
            label="📋 Download JSON",
            data=json_data,
            file_name="brutalyze_report.json",
            mime="application/json"
        )
    
    with col3:
        # Alerts Download
        alerts_text = "\n".join(result.get("alerts", []))
        st.download_button(
            label="🚨 Download Alerts",
            data=alerts_text,
            file_name="brutalyze_alerts.txt",
            mime="text/plain"
        )
    
    # Display classified logs
    st.header("📋 Detailed Log Analysis")
    
    for category, logs in result["classified"].items():
        if logs:  # Only show categories with logs
            with st.expander(f"{category} ({len(logs)} entries)", expanded=False):
                # Create DataFrame for this category
                log_data = []
                for log in logs:
                    loc = log.get("location", {})
                    log_data.append({
                        "Timestamp": log.get("timestamp", ""),
                        "User": log.get("user", "-"),
                        "IP": log.get("ip", "-"),
                        "Country": loc.get("country", "-"),
                        "Region": loc.get("region", "-"),
                        "City": loc.get("city", "-"),
                        "Raw Log": log.get("raw", "")
                    })
                
                if log_data:
                    df = pd.DataFrame(log_data)
                    st.dataframe(df, use_container_width=True)
    
    # Clean up temporary file
    if uploaded_file is not None:
        import os
        if os.path.exists("temp_upload.log"):
            os.remove("temp_upload.log")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>🛡️ <strong>Brutalyze Web</strong> - Privacy-focused log analysis</p>
        <p>No data is stored on the server. All analysis is done in-memory.</p>
    </div>
    """, 
    unsafe_allow_html=True
)

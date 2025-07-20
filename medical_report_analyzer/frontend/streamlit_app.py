import streamlit as st
import requests
import json
from pathlib import Path
import time

st.set_page_config(
    page_title="Medical Report Analyzer",
    page_icon="🏥",
    layout="wide"
)

def main():
    st.title("🏥 Medical Report Analysis System")
    
    # Sidebar
    st.sidebar.header("About")
    st.sidebar.info(
        "This application analyzes medical reports using AI to provide "
        "insights, summaries, and key findings."
    )
    
    # Main content
    uploaded_file = st.file_uploader(
        "Upload Medical Report (PDF)", 
        type="pdf",
        help="Upload a medical report in PDF format"
    )
    
    if uploaded_file is not None:
        with st.spinner("Analyzing report..."):
            try:
                files = {'file': uploaded_file}
                response = requests.post(
                    'http://localhost:5000/analyze',
                    files=files,
                    timeout=30
                )
                
                if response.status_code == 200:
                    analysis = response.json()
                    
                    # Display results in tabs
                    tab1, tab2 = st.tabs(["Analysis", "Document Info"])
                    
                    with tab1:
                        st.markdown(analysis['analysis'])
                    
                    with tab2:
                        st.info(f"Document Statistics:")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Text Chunks", analysis['chunks'])
                        with col2:
                            st.metric("Document Length", analysis['document_length'])
                        
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error occurred')}")
                    
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {str(e)}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
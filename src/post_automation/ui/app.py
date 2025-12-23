"""Main Streamlit application."""

import streamlit as st

st.set_page_config(
    page_title="Post Automation Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Main page
st.title("🤖 Post Automation Platform")
st.markdown("---")

st.markdown(
    """
    ## Welcome to the Post Automation Platform

    This platform provides AI-powered tools for content analysis and PowerPoint automation:

    ### Features

    **📝 AI Content Detection**
    - Detect AI-generated text with confidence scores
    - Analyze PowerPoint presentations slide-by-slide
    - Support for both text input and file uploads

    **📊 PowerPoint Modification**
    - Automatically replace AI-detected content
    - Apply custom styles and formatting
    - Download modified presentations

    **🔧 n8n Workflow Integration**
    - REST API endpoints for automation
    - Seamless integration with n8n workflows
    - Health monitoring and status checks

    ### Getting Started

    Use the sidebar to navigate between different features:

    1. **AI Detection** - Analyze text or PowerPoint files for AI-generated content
    2. **PPT Modification** - Modify presentations with AI detection and styling
    3. **About** - Learn more about the project

    ### API Documentation

    For n8n integration and API usage, visit:
    - Swagger UI: `http://localhost:8000/docs`
    - ReDoc: `http://localhost:8000/redoc`

    ---

    **Version:** 0.1.0
    **Project:** Post Automation
    **Purpose:** Homework Assignment - AI Detection & PowerPoint Automation
    """
)

st.info(
    "👈 Select a page from the sidebar to get started!",
    icon="ℹ️"
)

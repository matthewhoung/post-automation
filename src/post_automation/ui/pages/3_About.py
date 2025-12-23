"""About page for Streamlit UI."""

import streamlit as st

st.set_page_config(page_title="About", page_icon="📖", layout="wide")

st.title("📖 About Post Automation Platform")
st.markdown("---")

# Project Overview
st.markdown("## 🎯 Project Overview")
st.markdown(
    """
    **Post Automation Platform** is a comprehensive solution for AI content detection
    and PowerPoint automation, designed as a homework assignment with three main components:

    1. **AI Content Detection** - Identify AI-generated vs human-written text
    2. **PowerPoint Modification** - Automatically modify presentations
    3. **n8n Workflow Integration** - REST API for automation workflows
    """
)

st.markdown("---")

# Features
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔍 AI Detection Features")
    st.markdown(
        """
        - Text analysis with confidence scores
        - PowerPoint slide-by-slide analysis
        - Multiple model support
        - Batch processing
        - Real-time results
        """
    )

    st.markdown("### 📊 PowerPoint Features")
    st.markdown(
        """
        - Automatic content replacement
        - Style modifications (fonts, colors)
        - Text extraction and analysis
        - Table support
        - Download modified files
        """
    )

with col2:
    st.markdown("### 🔧 Integration Features")
    st.markdown(
        """
        - REST API endpoints
        - n8n workflow support
        - Health monitoring
        - OpenAPI documentation
        - CORS enabled
        """
    )

    st.markdown("### 🎨 UI Features")
    st.markdown(
        """
        - Multi-page Streamlit app
        - File upload support
        - Real-time processing
        - Progress indicators
        - Download capabilities
        """
    )

st.markdown("---")

# Technical Stack
st.markdown("## 🛠️ Technical Stack")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Backend")
    st.markdown(
        """
        - **Python 3.11+**
        - **FastAPI** - REST API
        - **Streamlit** - Web UI
        - **python-pptx** - PowerPoint
        """
    )

with col2:
    st.markdown("### AI/ML")
    st.markdown(
        """
        - **HuggingFace Transformers**
        - **PyTorch**
        - **RoBERTa Models**
        - **Content Generation**
        """
    )

with col3:
    st.markdown("### Tools")
    st.markdown(
        """
        - **UV** - Package management
        - **Pydantic** - Validation
        - **Pytest** - Testing
        - **Black/Ruff** - Formatting
        """
    )

st.markdown("---")

# Architecture
st.markdown("## 🏗️ Architecture")

st.markdown(
    """
    The platform follows a **layered architecture** with clear separation of concerns:

    ```
    ┌─────────────────────────────────────────────┐
    │         Entry Points (Multi-mode)            │
    ├──────────────────┬──────────────────────────┤
    │  Streamlit UI    │      FastAPI REST API    │
    │  (Demo/Testing)  │      (n8n Integration)   │
    └────────┬─────────┴──────────┬───────────────┘
             │                    │
             └────────┬───────────┘
                      │
    ┌─────────────────▼─────────────────┐
    │        Core Business Logic         │
    ├────────────────────────────────────┤
    │  • AI Detector                     │
    │  • PPT Analyzer                    │
    │  • PPT Modifier                    │
    │  • Content Generator               │
    └────────────────────────────────────┘
    ```

    **Key Principles:**
    - Framework-independent core logic
    - Dependency inversion
    - Single responsibility
    - Easy testing and maintenance
    """
)

st.markdown("---")

# API Endpoints
st.markdown("## 🌐 API Endpoints")

st.markdown("### Detection Endpoints")
st.code(
    """
POST /api/detect/text
    - Detect AI in plain text
    - Input: JSON with text
    - Output: Detection result

POST /api/detect/pptx
    - Detect AI in PowerPoint
    - Input: File upload
    - Output: Per-slide results
""",
    language="text",
)

st.markdown("### Modification Endpoints")
st.code(
    """
POST /api/modify/pptx
    - Modify PowerPoint file
    - Input: File + parameters
    - Output: Modified PPTX file
""",
    language="text",
)

st.markdown("### Utility Endpoints")
st.code(
    """
GET /api/health
    - Health check
    - Output: Service status
""",
    language="text",
)

st.markdown("---")

# Project Structure
st.markdown("## 📁 Project Structure")

st.code(
    """
post-automation/
├── src/post_automation/
│   ├── core/           # Business logic
│   ├── models/         # Data models
│   ├── api/            # FastAPI routes
│   ├── ui/             # Streamlit pages
│   ├── workflows/      # n8n workflows
│   └── utils/          # Utilities
├── tests/              # Test suite
├── docs/               # Documentation
└── scripts/            # Helper scripts
""",
    language="text",
)

st.markdown("---")

# Version and Credits
col1, col2 = st.columns(2)

with col1:
    st.markdown("## 📌 Version Information")
    st.markdown(
        """
        - **Version:** 0.1.0
        - **Python:** 3.11.14+
        - **License:** MIT
        """
    )

with col2:
    st.markdown("## 🎓 Project Type")
    st.markdown(
        """
        - **Type:** Homework Assignment
        - **Purpose:** AI Detection & Automation
        - **Deployment:** Streamlit Cloud
        """
    )

st.markdown("---")

# Links
st.markdown("## 🔗 Useful Links")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Documentation")
    st.markdown("- [API Docs](/docs)")
    st.markdown("- [Swagger UI](http://localhost:8000/docs)")
    st.markdown("- [ReDoc](http://localhost:8000/redoc)")

with col2:
    st.markdown("### Resources")
    st.markdown("- [HuggingFace](https://huggingface.co)")
    st.markdown("- [FastAPI](https://fastapi.tiangolo.com)")
    st.markdown("- [Streamlit](https://streamlit.io)")

with col3:
    st.markdown("### Tools")
    st.markdown("- [python-pptx](https://python-pptx.readthedocs.io)")
    st.markdown("- [n8n](https://n8n.io)")
    st.markdown("- [UV](https://github.com/astral-sh/uv)")

st.markdown("---")

st.info(
    "For more information, check out the documentation in the `/docs` directory.",
    icon="📚"
)

# Post Automation Platform

AI-powered content detection and PowerPoint automation with n8n integration.

## Overview

This project is a comprehensive solution for detecting AI-generated content and automating PowerPoint modifications. It consists of three main components:

1. **AI Content Detection** - Identify AI-generated vs human-written text using HuggingFace transformers
2. **PowerPoint Modification** - Automatically replace AI-detected content and apply style changes
3. **n8n Workflow Integration** - REST API for automation workflows

## Features

### AI Detection
- Detect AI-generated content in plain text
- Analyze PowerPoint presentations slide-by-slide
- Confidence scores and detailed results
- Support for multiple HuggingFace models

### PowerPoint Automation
- Extract text from PPTX files
- Replace AI-detected content with alternatives
- Apply style modifications (fonts, colors)
- Preserve original formatting where possible

### Integration
- FastAPI REST API for n8n workflows
- Streamlit web UI for demos
- OpenAPI documentation
- CORS-enabled for external integrations

## Tech Stack

- **Python 3.11+** - Core language
- **FastAPI** - REST API framework
- **Streamlit** - Web UI
- **HuggingFace Transformers** - AI detection models
- **python-pptx** - PowerPoint manipulation
- **UV** - Package management
- **Pydantic** - Data validation

## Quick Start

### Prerequisites

- Python 3.11.14 or higher
- UV package manager
- HuggingFace account and API token

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/post-automation.git
cd post-automation
```

2. Install dependencies with UV:
```bash
uv sync
```

3. Create `.env` file from example:
```bash
cp .env.example .env
```

4. Update `.env` with your HuggingFace token:
```bash
HF_TOKEN=your_huggingface_token_here
```

### Running the Application

#### Option 1: Streamlit UI (Demo)

```bash
./scripts/run_ui.sh
```

Visit `http://localhost:8501` to use the web interface.

#### Option 2: FastAPI Server (for n8n)

```bash
./scripts/run_api.sh
```

API available at `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Generate n8n Workflow

```bash
python scripts/generate_workflow.py --api-url http://localhost:8000 --output workflows/workflow.json
```

Import `workflows/workflow.json` into n8n to use the automation workflow.

## Project Structure

```
post-automation/
├── src/post_automation/       # Main package
│   ├── core/                  # Business logic
│   │   ├── ai_detector.py     # AI content detection
│   │   ├── ppt_analyzer.py    # PowerPoint text extraction
│   │   ├── ppt_modifier.py    # PowerPoint modification
│   │   └── content_generator.py # Alternative content generation
│   ├── models/                # Data models
│   ├── api/                   # FastAPI REST API
│   ├── ui/                    # Streamlit web UI
│   ├── workflows/             # n8n workflow generation
│   └── utils/                 # Utilities
├── tests/                     # Test suite
├── docs/                      # Documentation
├── scripts/                   # Helper scripts
└── workflows/                 # Generated n8n workflows
```

## API Endpoints

### Detection

**POST /api/detect/text**
```json
{
  "text": "Your text here",
  "model": "roberta-base-openai-detector"
}
```

**POST /api/detect/pptx**
- Upload: PowerPoint file (.pptx)
- Returns: Per-slide AI detection results

### Modification

**POST /api/modify/pptx**
- Upload: PowerPoint file (.pptx)
- Parameters:
  - `replace_ai_content`: boolean (default: true)
  - `font_name`: string (optional)
  - `text_color`: hex color (optional)
  - `confidence_threshold`: float 0.0-1.0 (default: 0.7)
- Returns: Modified PowerPoint file

### Utility

**GET /api/health**
- Returns: Service health status

## Configuration

All settings are configured via environment variables in `.env`:

```bash
# HuggingFace
HF_TOKEN=your_token
HF_MODEL_NAME=roberta-base-openai-detector

# API
API_HOST=0.0.0.0
API_PORT=8000

# Streamlit
STREAMLIT_PORT=8501

# File Upload
MAX_UPLOAD_SIZE_MB=10

# Logging
LOG_LEVEL=INFO
```

## Development

### Install Development Dependencies

```bash
uv sync --all-extras
```

### Run Tests

```bash
pytest
```

### Code Formatting

```bash
black src/ tests/
ruff check src/ tests/
```

### Type Checking

```bash
mypy src/
```

## Deployment

### Streamlit Cloud

1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Set HF_TOKEN in Streamlit secrets
4. Deploy

### FastAPI (Docker)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install uv
RUN uv sync

CMD ["uvicorn", "src.post_automation.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Documentation

- [API Documentation](docs/API.md)
- [Development Guide](docs/DEVELOPMENT.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Architecture Overview](docs/ARCHITECTURE.md)

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- HuggingFace for transformer models
- FastAPI for the excellent web framework
- Streamlit for the beautiful UI
- python-pptx for PowerPoint manipulation
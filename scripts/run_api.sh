#!/bin/bash
# Run FastAPI server

echo "🚀 Starting Post Automation API..."

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "📝 Please update .env with your HuggingFace token"
fi

# Run with uvicorn
uvicorn src.post_automation.api.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload

#!/bin/bash
# Run Streamlit UI

echo "🎨 Starting Post Automation UI..."

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "📝 Please update .env with your HuggingFace token"
fi

# Run Streamlit
streamlit run src/post_automation/ui/app.py \
    --server.port 8501 \
    --server.address 0.0.0.0

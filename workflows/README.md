# n8n Workflows

This directory contains generated n8n workflow JSON files for automating post-automation tasks.

## Available Workflows

### workflow.json

Main workflow that performs:
1. Receives PowerPoint file via webhook
2. Detects AI-generated content
3. Modifies presentation if AI content is found
4. Returns results

### Generating Workflows

Use the workflow generator script:

```bash
python scripts/generate_workflow.py --api-url http://localhost:8000 --output workflows/workflow.json
```

Options:
- `--api-url`: Base URL for the API (default: http://localhost:8000)
- `--output`: Output file path (default: workflows/workflow.json)
- `--confidence`: AI confidence threshold (default: 0.7)
- `--simple`: Generate simple detection-only workflow

## Importing into n8n

1. Open n8n
2. Click "Import from File"
3. Select `workflow.json`
4. Activate the workflow

## Workflow Configuration

Before using the workflow, ensure:
1. FastAPI server is running (`./scripts/run_api.sh`)
2. API_BASE_URL environment variable is set in n8n
3. Webhook is activated

## Testing the Workflow

Test the webhook:

```bash
curl -X POST http://localhost:5678/webhook-test/process-presentation \
  -F "file=@test.pptx"
```

## Workflow Diagram

```
Webhook Trigger
    ↓
Detect AI Content (POST /api/detect/pptx)
    ↓
Check AI Detected?
    ├─ Yes → Modify Presentation (POST /api/modify/pptx) → Respond Modified
    └─ No  → Respond No Action
```

## Customization

Edit the generated JSON to:
- Change confidence thresholds
- Add notifications
- Integrate with other services
- Modify response format

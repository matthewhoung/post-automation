# Architecture Decision Record: REST API Design

**Date**: 2025-12-23
**Status**: Accepted
**Decision Makers**: Project Team

---

## Context

Need to provide REST API endpoints for n8n workflow automation. The API must support:
1. AI content detection (text and PPTX files)
2. PowerPoint modification
3. Health check for monitoring

n8n will call these endpoints via HTTP Request nodes.

---

## Decision

Build REST API using **FastAPI** with the following endpoint structure:

```
POST /api/detect/text         - Detect AI in plain text
POST /api/detect/pptx         - Detect AI in PowerPoint file
POST /api/modify/pptx         - Modify PowerPoint file
GET  /api/health              - Health check
```

### Technology Choice: FastAPI

**Why FastAPI over Flask/Django?**

| Feature | FastAPI | Flask | Django |
|---------|---------|-------|--------|
| Type hints | ✅ Native | ❌ No | ❌ No |
| Auto docs | ✅ OpenAPI | ❌ Manual | ❌ Manual |
| Async support | ✅ Native | ⚠️ Limited | ⚠️ Limited |
| Learning curve | ✅ Low | ✅ Low | ❌ High |
| File uploads | ✅ Easy | ✅ Easy | ✅ Easy |
| Size/Speed | ✅ Fast | ✅ Fast | ❌ Heavy |

**Verdict**: FastAPI provides best DX with automatic OpenAPI docs and type safety.

---

## Endpoint Design

### 1. Text Detection Endpoint

**Endpoint**: `POST /api/detect/text`

**Request**:
```json
{
  "text": "The quick brown fox jumps over the lazy dog...",
  "model": "roberta-base-openai-detector"  // optional
}
```

**Response**:
```json
{
  "is_ai_generated": true,
  "confidence": 0.87,
  "label": "AI",
  "model_name": "roberta-base-openai-detector"
}
```

**Implementation**:
```python
from pydantic import BaseModel

class TextDetectionRequest(BaseModel):
    text: str
    model: str = "roberta-base-openai-detector"

class DetectionResponse(BaseModel):
    is_ai_generated: bool
    confidence: float
    label: str
    model_name: str

@router.post("/detect/text", response_model=DetectionResponse)
async def detect_text(request: TextDetectionRequest):
    detector = AIDetector(model_name=request.model)
    result = detector.detect(request.text)
    return DetectionResponse(**result.dict())
```

---

### 2. PPTX Detection Endpoint

**Endpoint**: `POST /api/detect/pptx`

**Request**: `multipart/form-data` with file upload

**Response**:
```json
{
  "file_name": "presentation.pptx",
  "total_slides": 10,
  "ai_slides": 6,
  "human_slides": 4,
  "slides": [
    {
      "slide_number": 0,
      "text": "Introduction to AI...",
      "detection": {
        "is_ai_generated": true,
        "confidence": 0.92,
        "label": "AI"
      }
    },
    ...
  ]
}
```

**Implementation**:
```python
from fastapi import UploadFile, File

class SlideDetectionResponse(BaseModel):
    slide_number: int
    text: str
    detection: DetectionResponse

class PresentationDetectionResponse(BaseModel):
    file_name: str
    total_slides: int
    ai_slides: int
    human_slides: int
    slides: List[SlideDetectionResponse]

@router.post("/detect/pptx", response_model=PresentationDetectionResponse)
async def detect_pptx(file: UploadFile = File(...)):
    # Save temp file
    temp_path = await save_upload(file)

    # Extract text
    analyzer = PPTAnalyzer()
    slides_text = analyzer.extract_text_from_pptx(temp_path)

    # Detect AI in each slide
    detector = AIDetector()
    results = []
    ai_count = 0

    for slide in slides_text:
        detection = detector.detect(slide.text)
        results.append(SlideDetectionResponse(
            slide_number=slide.slide_number,
            text=slide.text,
            detection=detection
        ))
        if detection.is_ai_generated:
            ai_count += 1

    return PresentationDetectionResponse(
        file_name=file.filename,
        total_slides=len(slides_text),
        ai_slides=ai_count,
        human_slides=len(slides_text) - ai_count,
        slides=results
    )
```

---

### 3. PPTX Modification Endpoint

**Endpoint**: `POST /api/modify/pptx`

**Request**: `multipart/form-data`
- `file`: PPTX file (required)
- `replace_ai_content`: boolean (optional, default: true)
- `font_name`: string (optional)
- `text_color`: string (optional, hex color)

**Response**: Binary PPTX file

**Implementation**:
```python
from fastapi.responses import FileResponse

@router.post("/modify/pptx")
async def modify_pptx(
    file: UploadFile = File(...),
    replace_ai_content: bool = True,
    font_name: Optional[str] = None,
    text_color: Optional[str] = None
):
    # Save uploaded file
    temp_input = await save_upload(file)

    # Detect and replace AI content
    replacements = []
    if replace_ai_content:
        analyzer = PPTAnalyzer()
        slides = analyzer.extract_text_from_pptx(temp_input)

        detector = AIDetector()
        generator = ContentGenerator()

        for slide in slides:
            detection = detector.detect(slide.text)
            if detection.is_ai_generated and detection.confidence > 0.7:
                new_text = generator.generate(slide.text)
                replacements.append(Replacement(
                    slide_num=slide.slide_number,
                    old_text=slide.text,
                    new_text=new_text
                ))

    # Apply modifications
    modifier = PPTModifier(temp_input)

    if replacements:
        modifier.replace_content(replacements)

    if font_name or text_color:
        style_config = StyleConfig(
            font_name=font_name,
            color_scheme=ColorScheme(text_color=text_color) if text_color else None
        )
        modifier.modify_styles(style_config)

    # Save modified file
    output_path = f"/tmp/{uuid.uuid4()}.pptx"
    modifier.save(output_path)

    # Return file
    return FileResponse(
        output_path,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename=f"modified_{file.filename}"
    )
```

---

### 4. Health Check Endpoint

**Endpoint**: `GET /api/health`

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-23T10:30:00Z",
  "version": "0.1.0",
  "models_loaded": true
}
```

**Implementation**:
```python
from datetime import datetime

@router.get("/health")
async def health_check():
    # Check if models can be loaded
    try:
        detector = AIDetector()
        models_ok = True
    except Exception:
        models_ok = False

    return {
        "status": "healthy" if models_ok else "degraded",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "0.1.0",
        "models_loaded": models_ok
    }
```

---

## CORS Configuration

n8n runs on different domain, so CORS must be enabled.

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify n8n domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Security Note**: In production, replace `["*"]` with actual n8n domain(s).

---

## Error Handling

### Standard Error Response
```json
{
  "detail": "Error message here",
  "error_type": "ValidationError",
  "timestamp": "2025-12-23T10:30:00Z"
}
```

### HTTP Status Codes
- `200 OK`: Success
- `400 Bad Request`: Invalid input (wrong file type, missing fields)
- `413 Payload Too Large`: File size exceeds limit
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error (model loading failed, etc.)

### Implementation
```python
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": str(exc),
            "error_type": type(exc).__name__,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    )
```

---

## File Upload Handling

### Size Limits
```python
from fastapi import HTTPException

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

async def save_upload(file: UploadFile) -> str:
    # Check size
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File size exceeds {MAX_FILE_SIZE / 1024 / 1024}MB limit"
        )

    # Validate extension
    if not file.filename.endswith('.pptx'):
        raise HTTPException(
            status_code=400,
            detail="Only .pptx files are supported"
        )

    # Save to temp file
    temp_path = f"/tmp/{uuid.uuid4()}_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(contents)

    return temp_path
```

### Cleanup
```python
import atexit
import glob

def cleanup_temp_files():
    for file in glob.glob("/tmp/*.pptx"):
        try:
            os.remove(file)
        except:
            pass

atexit.register(cleanup_temp_files)
```

---

## API Documentation

FastAPI auto-generates OpenAPI docs:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

This is useful for:
1. Testing endpoints manually
2. Sharing API spec with team
3. Importing into n8n (OpenAPI connector)

---

## n8n Integration Example

### Workflow Structure
```json
{
  "nodes": [
    {
      "name": "Trigger",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "process-pptx"
      }
    },
    {
      "name": "Detect AI Content",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "http://api.example.com/api/detect/pptx",
        "sendBinaryData": true,
        "binaryPropertyName": "data"
      }
    },
    {
      "name": "Modify Presentation",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "http://api.example.com/api/modify/pptx",
        "sendBinaryData": true,
        "binaryPropertyName": "data",
        "options": {
          "queryParameters": {
            "replace_ai_content": true,
            "font_name": "Arial"
          }
        }
      }
    }
  ]
}
```

---

## Testing Strategy

### Unit Tests
Test individual route functions with mocked dependencies.

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_detect_text():
    response = client.post("/api/detect/text", json={
        "text": "Sample text here"
    })
    assert response.status_code == 200
    data = response.json()
    assert "is_ai_generated" in data
    assert "confidence" in data
```

### Integration Tests
Test end-to-end with actual files.

```python
def test_detect_pptx():
    with open("tests/fixtures/sample.pptx", "rb") as f:
        response = client.post(
            "/api/detect/pptx",
            files={"file": ("sample.pptx", f, "application/vnd.openxmlformats-officedocument.presentationml.presentation")}
        )
    assert response.status_code == 200
    data = response.json()
    assert data["total_slides"] > 0
```

---

## Deployment Considerations

### Running the API
```bash
uvicorn src.post_automation.api.main:app --host 0.0.0.0 --port 8000
```

### Production Settings
```python
# Disable auto-reload in production
# Use Gunicorn with Uvicorn workers
gunicorn src.post_automation.api.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000
```

### Environment Variables
- `API_HOST`: Default 0.0.0.0
- `API_PORT`: Default 8000
- `API_WORKERS`: Number of worker processes
- `CORS_ORIGINS`: Allowed origins (comma-separated)
- `MAX_UPLOAD_SIZE_MB`: File size limit

---

## Consequences

### Positive
- **Auto-documentation**: OpenAPI docs generated automatically
- **Type safety**: Pydantic models catch errors early
- **Easy testing**: TestClient makes integration tests simple
- **n8n compatible**: Standard REST API works with n8n HTTP nodes

### Negative
- **File storage**: Need to manage temporary files
- **Memory**: Large files might cause memory issues
- **Concurrency**: Model loading is not thread-safe (need singleton)

### Mitigations
- Use async file handling
- Implement file size limits
- Use dependency injection for model loading
- Regular cleanup of temp files

---

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [n8n HTTP Request Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/)
- [OpenAPI Specification](https://swagger.io/specification/)

# Architecture Decision Record: AI Content Detection

**Date**: 2025-12-23
**Status**: Accepted
**Decision Makers**: Project Team

---

## Context

Need to detect whether text is AI-generated or human-written. The detection must work for:
1. Standalone text input
2. Text extracted from PowerPoint slides

HuggingFace token is available in environment, suggesting use of HuggingFace models.

---

## Decision

Use **HuggingFace Transformers** with a pre-trained AI detection model.

**Primary Model**: `roberta-base-openai-detector`
**Alternative Models**:
- `Hello-SimpleAI/chatgpt-detector-roberta` (ChatGPT-specific)
- `andreas122001/roberta-mixed-detector` (Multi-model detection)

### Implementation Approach

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class AIDetector:
    def __init__(self, model_name: str, hf_token: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_token)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name, token=hf_token)

    def detect(self, text: str) -> DetectionResult:
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        outputs = self.model(**inputs)
        probabilities = torch.softmax(outputs.logits, dim=-1)

        return DetectionResult(
            is_ai_generated=probabilities[0][1] > 0.5,
            confidence=float(probabilities[0][1]),
            label="AI" if probabilities[0][1] > 0.5 else "Human"
        )
```

---

## Rationale

### Why HuggingFace Transformers?
✅ **Chosen**
- Pre-trained models available for AI detection
- HF_TOKEN already configured in .env
- Good accuracy for GPT-3/ChatGPT detection
- Active community and model updates

### Why Not OpenAI API?
❌ **Rejected**
- Requires additional API key and costs
- OpenAI doesn't provide AI detection API (they shut down their detector)
- Dependency on external service

### Why Not Build Custom Model?
❌ **Rejected**
- Requires training data collection
- Time-consuming for homework assignment
- Lower accuracy than pre-trained models
- Need ML expertise

### Why Not GPTZero/Other Paid Services?
❌ **Rejected**
- Cost per request
- External dependency
- Rate limits
- Not suitable for self-hosted solution

---

## Model Selection Criteria

| Model | Accuracy | Speed | Size | Use Case |
|-------|----------|-------|------|----------|
| roberta-base-openai-detector | High | Medium | 500MB | General GPT detection |
| chatgpt-detector-roberta | Very High | Medium | 500MB | ChatGPT-specific |
| roberta-mixed-detector | High | Medium | 500MB | Multiple AI models |

**Recommendation**: Start with `roberta-base-openai-detector`, make configurable via .env

---

## Technical Considerations

### Model Loading
- **Cache models** to avoid re-downloading
- Use `transformers` cache directory: `~/.cache/huggingface/`
- Lazy load on first request (don't block startup)

### Text Preprocessing
- **Chunking**: Split long texts into 512-token chunks
- **Aggregation**: Average confidence scores across chunks
- **Minimum length**: Require at least 50 tokens for reliable detection

### Confidence Thresholds
- **High confidence**: > 0.8 (clearly AI or human)
- **Medium confidence**: 0.5 - 0.8 (likely AI or human)
- **Low confidence**: < 0.5 (uncertain)

### PowerPoint Integration
```python
def detect_in_pptx(pptx_path: str) -> List[SlideDetection]:
    slides_text = extract_text_from_pptx(pptx_path)
    results = []

    for slide in slides_text:
        detection = detector.detect(slide.text)
        results.append(SlideDetection(
            slide_number=slide.number,
            text=slide.text,
            detection=detection
        ))

    return results
```

---

## Consequences

### Positive
- **No external costs**: Self-hosted model
- **Privacy**: No data sent to third parties
- **Flexibility**: Can swap models easily
- **Offline capable**: Works without internet (after initial download)

### Negative
- **Model size**: ~500MB download
- **Memory usage**: ~2GB RAM during inference
- **Startup time**: 5-10 seconds to load model
- **Accuracy limitations**: Not perfect, especially for mixed content

### Mitigations
- **Model caching**: Cache loaded model in memory (singleton pattern)
- **Streamlit deployment**: May need to upgrade to higher tier for memory
- **Alternative**: Use HuggingFace Inference API for Streamlit Cloud (free tier)

---

## Alternatives for Streamlit Deployment

If memory limits are hit on Streamlit Cloud:

### Option 1: HuggingFace Inference API
```python
import requests

def detect_via_api(text: str, hf_token: str) -> DetectionResult:
    API_URL = "https://api-inference.huggingface.co/models/roberta-base-openai-detector"
    headers = {"Authorization": f"Bearer {hf_token}"}
    response = requests.post(API_URL, headers=headers, json={"inputs": text})
    return parse_response(response.json())
```
**Pros**: No memory footprint
**Cons**: Rate limits, latency

### Option 2: Quantized Model
Use smaller, quantized version of the model (8-bit or 4-bit)
```python
from transformers import BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(load_in_8bit=True)
model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    quantization_config=quantization_config
)
```
**Pros**: 50% memory reduction
**Cons**: Slight accuracy decrease

---

## Data Models

```python
from pydantic import BaseModel

class DetectionResult(BaseModel):
    is_ai_generated: bool
    confidence: float  # 0.0 to 1.0
    label: str  # "AI" or "Human"
    model_name: str

class SlideDetection(BaseModel):
    slide_number: int
    text: str
    detection: DetectionResult

class PresentationDetection(BaseModel):
    file_name: str
    total_slides: int
    ai_slides: int
    human_slides: int
    slides: List[SlideDetection]
```

---

## Testing Strategy

### Unit Tests
```python
def test_detect_ai_content():
    detector = AIDetector(model_name="roberta-base-openai-detector")
    ai_text = "The quick brown fox jumps over the lazy dog in a systematic manner."
    result = detector.detect(ai_text)
    assert result.confidence > 0.0
    assert result.label in ["AI", "Human"]

def test_detect_short_text():
    detector = AIDetector(model_name="roberta-base-openai-detector")
    short_text = "Hi"
    # Should handle gracefully
    result = detector.detect(short_text)
    assert result is not None
```

### Integration Tests
- Test with known AI-generated samples
- Test with known human-written samples
- Test with mixed content

### Performance Tests
- Measure inference time
- Measure memory usage
- Test with long documents (10k+ words)

---

## References

- [RoBERTa: A Robustly Optimized BERT](https://arxiv.org/abs/1907.11692)
- [OpenAI GPT Detector (deprecated)](https://openai.com/blog/new-ai-classifier-for-indicating-ai-written-text)
- [HuggingFace Model Hub](https://huggingface.co/models?pipeline_tag=text-classification&search=ai%20detector)

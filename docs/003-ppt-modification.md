# Architecture Decision Record: PowerPoint Modification

**Date**: 2025-12-23
**Status**: Accepted
**Decision Makers**: Project Team

---

## Context

Need to modify PowerPoint presentations by:
1. Replacing AI-detected content with alternative text
2. Changing styles (fonts, colors, layouts)

Requirements:
- Use `python-pptx` library
- Support .pptx files (Office Open XML format)
- Preserve presentation structure where possible

---

## Decision

Use **python-pptx** for PowerPoint manipulation with two distinct modification strategies:

1. **Content Replacement**: Replace text runs identified as AI-generated
2. **Style Modification**: Change fonts, colors, and formatting

### Implementation Architecture

```python
class PPTModifier:
    def __init__(self, pptx_path: str):
        self.presentation = Presentation(pptx_path)

    def replace_content(self, replacements: List[Replacement]) -> None:
        """Replace specific text content in slides."""
        for replacement in replacements:
            self._replace_in_slide(replacement.slide_num,
                                  replacement.old_text,
                                  replacement.new_text)

    def modify_styles(self, style_config: StyleConfig) -> None:
        """Apply style changes to presentation."""
        if style_config.font_name:
            self._change_fonts(style_config.font_name)
        if style_config.color_scheme:
            self._change_colors(style_config.color_scheme)

    def save(self, output_path: str) -> None:
        """Save modified presentation."""
        self.presentation.save(output_path)
```

---

## Rationale

### Why python-pptx?
✅ **Chosen**
- Actively maintained (last update 2024)
- Pure Python (no system dependencies)
- Supports Office Open XML (.pptx)
- Good documentation and examples
- Works with UV/pip

### Why Not Other Libraries?

**python-office** ❌
- Less mature
- Fewer examples
- Limited documentation

**aspose.slides** ❌
- Commercial license required
- Expensive for homework
- Overkill for simple modifications

**LibreOffice UNO** ❌
- Requires LibreOffice installation
- Complex API
- Harder to deploy (system dependency)

**Direct XML manipulation** ❌
- Error-prone
- Hard to maintain
- Office Open XML is complex

---

## Modification Strategies

### 1. Content Replacement Strategy

**Approach A: Full Text Replacement** (Chosen)
```python
def _replace_in_slide(self, slide_num: int, old_text: str, new_text: str):
    slide = self.presentation.slides[slide_num]
    for shape in slide.shapes:
        if hasattr(shape, "text_frame"):
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    if old_text in run.text:
                        run.text = run.text.replace(old_text, new_text)
```

**Why not Approach B: Shape-level replacement?**
- Loses formatting within text runs
- Can't handle partial replacements

**Why not Approach C: Delete and recreate?**
- Loses all formatting
- Position and sizing issues

### 2. Style Modification Strategy

**Font Changes**:
```python
def _change_fonts(self, font_name: str):
    for slide in self.presentation.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text_frame"):
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        run.font.name = font_name
```

**Color Changes**:
```python
def _change_colors(self, color_scheme: ColorScheme):
    for slide in self.presentation.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text_frame"):
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        run.font.color.rgb = color_scheme.text_color
```

**Layout Changes**:
- More complex: requires understanding slide masters
- May skip for initial implementation
- Focus on text-level changes first

---

## Technical Considerations

### Text Extraction for Analysis
```python
class PPTAnalyzer:
    def extract_text_from_pptx(self, pptx_path: str) -> List[SlideText]:
        prs = Presentation(pptx_path)
        results = []

        for i, slide in enumerate(prs.slides):
            slide_text = []
            for shape in slide.shapes:
                if hasattr(shape, "text_frame"):
                    for paragraph in shape.text_frame.paragraphs:
                        text = paragraph.text
                        if text.strip():
                            slide_text.append(text)

            results.append(SlideText(
                slide_number=i,
                text=" ".join(slide_text),
                shape_count=len(slide.shapes)
            ))

        return results
```

### Preserving Formatting

**Challenge**: Replacement might break formatting
**Solution**: Work at run level, preserve run properties

```python
def _smart_replace(self, run, old_text: str, new_text: str):
    # Preserve font properties
    font_name = run.font.name
    font_size = run.font.size
    font_bold = run.font.bold
    font_italic = run.font.italic

    # Replace text
    run.text = run.text.replace(old_text, new_text)

    # Restore properties (python-pptx sometimes resets them)
    run.font.name = font_name
    run.font.size = font_size
    run.font.bold = font_bold
    run.font.italic = font_italic
```

### File Format Support

**Supported**: `.pptx` (Office Open XML)
**Not Supported**: `.ppt` (binary format), `.odp` (OpenDocument)

**Validation**:
```python
ALLOWED_EXTENSIONS = {".pptx"}

def validate_file(file_path: str) -> bool:
    ext = Path(file_path).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file format: {ext}")
    return True
```

---

## Data Models

```python
from pydantic import BaseModel
from typing import Optional

class Replacement(BaseModel):
    slide_num: int
    old_text: str
    new_text: str

class ColorScheme(BaseModel):
    text_color: str  # RGB hex: "#FF5733"
    background_color: Optional[str] = None

class StyleConfig(BaseModel):
    font_name: Optional[str] = "Calibri"
    font_size: Optional[int] = None
    color_scheme: Optional[ColorScheme] = None

class SlideText(BaseModel):
    slide_number: int
    text: str
    shape_count: int
```

---

## Consequences

### Positive
- **Simple API**: python-pptx is straightforward
- **No dependencies**: Pure Python, no system libs
- **Preserves structure**: Keeps slides, shapes intact
- **Format support**: Works with modern .pptx files

### Negative
- **Limited layout control**: Can't easily modify slide masters
- **No .ppt support**: Only .pptx (Office 2007+)
- **Complex shapes**: Charts, SmartArt are harder to modify
- **Formatting edge cases**: Some formatting might not preserve perfectly

### Mitigations
- **Documentation**: Document supported features clearly
- **Validation**: Check file format upfront
- **Graceful degradation**: Handle unsupported shapes gracefully
- **Testing**: Extensive tests with various PPTX files

---

## Limitations and Workarounds

### Limitation 1: No Chart Text Modification
**Issue**: Charts have their own data model
**Workaround**: Skip charts, focus on text shapes

### Limitation 2: Master Slide Changes Complex
**Issue**: Modifying slide masters affects all slides
**Workaround**: Apply styles per-slide instead

### Limitation 3: Images Can't Be Analyzed
**Issue**: OCR not included in python-pptx
**Workaround**: Phase 1 focuses on text only; note as future enhancement

### Limitation 4: Tables Need Special Handling
**Issue**: Tables have nested cell structure
**Workaround**: Implement table text extraction separately

```python
def _extract_table_text(self, shape):
    if shape.has_table:
        table = shape.table
        text_parts = []
        for row in table.rows:
            for cell in row.cells:
                text_parts.append(cell.text)
        return " ".join(text_parts)
    return ""
```

---

## Testing Strategy

### Unit Tests
```python
def test_replace_content():
    modifier = PPTModifier("sample.pptx")
    modifier.replace_content([
        Replacement(slide_num=0, old_text="AI text", new_text="Human text")
    ])
    modifier.save("output.pptx")

    # Verify
    prs = Presentation("output.pptx")
    slide_text = prs.slides[0].shapes[0].text
    assert "Human text" in slide_text
    assert "AI text" not in slide_text

def test_change_fonts():
    modifier = PPTModifier("sample.pptx")
    modifier.modify_styles(StyleConfig(font_name="Arial"))
    modifier.save("output.pptx")

    # Verify
    prs = Presentation("output.pptx")
    first_run = prs.slides[0].shapes[0].text_frame.paragraphs[0].runs[0]
    assert first_run.font.name == "Arial"
```

### Integration Tests
- Test with various PPTX templates
- Test with different content types (text, tables, charts)
- Test edge cases (empty slides, no text, etc.)

### Fixtures
- `tests/fixtures/simple.pptx` - Basic text slides
- `tests/fixtures/complex.pptx` - Mixed content (tables, charts)
- `tests/fixtures/formatted.pptx` - Heavy formatting

---

## Content Generation for Replacement

Two approaches for generating alternative content:

### Approach 1: HuggingFace Paraphrasing (Recommended)
```python
from transformers import pipeline

paraphraser = pipeline("text2text-generation", model="Vamsi/T5_Paraphrase_Paws")

def generate_alternative(text: str) -> str:
    result = paraphraser(f"paraphrase: {text}", max_length=len(text) * 2)
    return result[0]['generated_text']
```

### Approach 2: Rule-Based Transformation
```python
def simple_paraphrase(text: str) -> str:
    # Simple word substitutions
    replacements = {
        "utilize": "use",
        "in order to": "to",
        "due to the fact that": "because"
    }
    result = text
    for old, new in replacements.items():
        result = result.replace(old, new)
    return result
```

**Recommendation**: Start with Approach 2 (simple), optionally add Approach 1 if time permits.

---

## API Endpoint Design

```python
# FastAPI route
@router.post("/api/modify/pptx")
async def modify_presentation(
    file: UploadFile = File(...),
    replace_ai_content: bool = True,
    style_config: Optional[StyleConfig] = None
) -> FileResponse:
    # Save uploaded file
    temp_input = save_temp_file(file)

    # Detect AI content if needed
    if replace_ai_content:
        slides = ppt_analyzer.extract_text_from_pptx(temp_input)
        replacements = []
        for slide in slides:
            detection = ai_detector.detect(slide.text)
            if detection.is_ai_generated:
                new_content = content_generator.generate(slide.text)
                replacements.append(Replacement(
                    slide_num=slide.slide_number,
                    old_text=slide.text,
                    new_text=new_content
                ))

    # Modify
    modifier = PPTModifier(temp_input)
    if replacements:
        modifier.replace_content(replacements)
    if style_config:
        modifier.modify_styles(style_config)

    # Save
    temp_output = generate_temp_filename()
    modifier.save(temp_output)

    return FileResponse(temp_output, filename="modified.pptx")
```

---

## References

- [python-pptx Documentation](https://python-pptx.readthedocs.io/)
- [Office Open XML Specification](http://officeopenxml.com/anatomyofOOXML-pptx.php)
- [PresentationML Reference](https://docs.microsoft.com/en-us/office/open-xml/presentation/working-with-presentations)

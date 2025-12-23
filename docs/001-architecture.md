# Architecture Decision Record: Project Structure

**Date**: 2025-12-23
**Status**: Accepted
**Decision Makers**: Project Team

---

## Context

The post-automation project requires three distinct but related features:
1. AI content detection
2. PowerPoint modification
3. n8n workflow integration

We need to support multiple entry points (Streamlit UI for demo, FastAPI for workflow automation) while maintaining clean separation of concerns.

---

## Decision

Adopt a **layered architecture** with clear separation between:
1. **Core business logic** (`src/post_automation/core/`)
2. **API layer** (`src/post_automation/api/`)
3. **UI layer** (`src/post_automation/ui/`)
4. **Workflow generation** (`src/post_automation/workflows/`)

### Key Architectural Principles

**1. Framework-Independent Core**
- Business logic has NO dependencies on FastAPI or Streamlit
- Core modules can be tested independently
- Makes it easy to add new entry points (e.g., CLI, different web framework)

**2. Dependency Inversion**
```
┌─────────┐     ┌─────────┐
│   API   │     │   UI    │
└────┬────┘     └────┬────┘
     │               │
     └───────┬───────┘
             │
         ┌───▼────┐
         │  Core  │
         └────────┘
```
Both API and UI depend on Core, but Core doesn't know about them.

**3. Single Responsibility**
- `ai_detector.py`: ONLY AI detection logic
- `ppt_analyzer.py`: ONLY text extraction
- `ppt_modifier.py`: ONLY file modification
- API routes: ONLY HTTP handling
- Streamlit pages: ONLY UI rendering

---

## Rationale

### Why Not a Monolithic Structure?
❌ **Avoided**: Single `main.py` with all logic
- Hard to test
- Coupling between UI and business logic
- Can't reuse logic across entry points

### Why Not Microservices?
❌ **Avoided**: Separate services for detection, modification, workflow
- Overkill for homework assignment
- Deployment complexity
- Communication overhead

### Why Layered Monolith?
✅ **Chosen**: Modular monolith with clear layers
- Simple deployment (one codebase)
- Easy to test each layer
- Clear boundaries between concerns
- Can evolve to microservices if needed

---

## Consequences

### Positive
- **Testability**: Each layer can be tested independently
- **Flexibility**: Easy to add new entry points (CLI, different UI framework)
- **Maintainability**: Clear where to add new features
- **Reusability**: Core logic shared between API and UI

### Negative
- **Initial Setup**: More files and folders than a simple script
- **Learning Curve**: Team needs to understand layer boundaries

### Mitigations
- Clear documentation of architecture
- Example implementations in each layer
- Enforce through code reviews

---

## Alternatives Considered

### Alternative 1: Flask + Jinja Templates
**Rejected**: Streamlit requirement specified; Streamlit provides better demo UX

### Alternative 2: Django
**Rejected**: Too heavyweight; Django ORM not needed (no database), admin panel not required

### Alternative 3: Flat Structure
**Rejected**: Would mix concerns and make testing difficult

---

## Implementation Notes

### File Naming Convention
- Use underscores for Python modules: `ai_detector.py`
- Package name: `post_automation` (underscore, not hyphen)
- Match Python PEP 8 style guide

### Import Strategy
```python
# API imports from core
from post_automation.core.ai_detector import detect_ai_content

# UI imports from core
from post_automation.core.ppt_modifier import modify_styles

# Core imports only stdlib and third-party
# Core NEVER imports from api or ui
```

### Testing Strategy
- Core: Unit tests with mocked external APIs
- API: Integration tests with TestClient
- UI: Manual testing (Streamlit not easily testable)

---

## References

- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/)
- [Streamlit Multi-page Apps](https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app)

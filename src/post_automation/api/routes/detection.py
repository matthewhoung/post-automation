"""AI detection endpoints."""

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from post_automation.core.ai_detector import get_detector
from post_automation.core.ppt_analyzer import PPTAnalyzer
from post_automation.models.api_schemas import TextDetectionRequest
from post_automation.models.detection import DetectionResult
from post_automation.models.ppt import PresentationDetection, SlideDetection
from post_automation.utils.file_handler import cleanup_file, save_uploaded_file
from post_automation.utils.logger import setup_logger
from post_automation.utils.validators import ValidationError, validate_pptx_file, validate_text_input

logger = setup_logger(__name__)

router = APIRouter()


@router.post("/detect/text", response_model=DetectionResult)
async def detect_text(request: TextDetectionRequest):
    """
    Detect AI-generated content in plain text.

    Args:
        request: Text detection request.

    Returns:
        Detection result with confidence score.
    """
    try:
        # Validate input
        validate_text_input(request.text)

        # Get detector
        detector = get_detector(request.model)

        # Run detection
        result = detector.detect(request.text)

        logger.info(f"Text detection complete: {result.label} ({result.confidence:.2f})")

        return result

    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Text detection failed: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/detect/pptx", response_model=PresentationDetection)
async def detect_pptx(file: UploadFile = File(...)):
    """
    Detect AI-generated content in PowerPoint presentation.

    Args:
        file: PowerPoint file upload.

    Returns:
        Presentation detection results with per-slide breakdown.
    """
    temp_path = None

    try:
        # Read file content
        file_content = await file.read()

        # Validate file
        validate_pptx_file(file.filename or "unknown.pptx", len(file_content))

        # Save to temporary location
        temp_path = save_uploaded_file(file_content, file.filename or "upload.pptx")

        # Extract text from slides
        analyzer = PPTAnalyzer()
        slides_text = analyzer.extract_text_from_pptx(temp_path)

        # Detect AI content in each slide
        detector = get_detector()
        slide_detections = []
        ai_count = 0

        for slide_text in slides_text:
            if slide_text.text.strip():
                detection = detector.detect(slide_text.text)

                slide_detections.append(
                    SlideDetection(
                        slide_number=slide_text.slide_number,
                        text=slide_text.text,
                        detection=detection,
                    )
                )

                if detection.is_ai_generated:
                    ai_count += 1
            else:
                # Empty slide - mark as human (no AI detection)
                slide_detections.append(
                    SlideDetection(
                        slide_number=slide_text.slide_number,
                        text="",
                        detection=DetectionResult(
                            is_ai_generated=False,
                            confidence=0.0,
                            label="Human",
                            model_name=detector.model_name,
                        ),
                    )
                )

        # Build response
        result = PresentationDetection(
            file_name=file.filename or "unknown.pptx",
            total_slides=len(slides_text),
            ai_slides=ai_count,
            human_slides=len(slides_text) - ai_count,
            slides=slide_detections,
        )

        logger.info(
            f"PPTX detection complete: {ai_count}/{len(slides_text)} slides detected as AI"
        )

        return result

    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"PPTX detection failed: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        # Cleanup temporary file
        if temp_path:
            cleanup_file(temp_path)

"""PowerPoint modification endpoint."""

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse

from post_automation.core.ai_detector import get_detector
from post_automation.core.content_generator import ContentGenerator
from post_automation.core.ppt_analyzer import PPTAnalyzer
from post_automation.core.ppt_modifier import PPTModifier
from post_automation.models.ppt import ColorScheme, Replacement, StyleConfig
from post_automation.utils.file_handler import cleanup_file, generate_temp_filename, save_uploaded_file
from post_automation.utils.logger import setup_logger
from post_automation.utils.validators import ValidationError, validate_pptx_file

logger = setup_logger(__name__)

router = APIRouter()


@router.post("/modify/pptx")
async def modify_pptx(
    file: UploadFile = File(...),
    replace_ai_content: bool = Form(True),
    font_name: str = Form(None),
    text_color: str = Form(None),
    confidence_threshold: float = Form(0.7),
):
    """
    Modify PowerPoint presentation.

    Supports:
    - Replacing AI-detected content with alternatives
    - Changing fonts and colors

    Args:
        file: PowerPoint file upload.
        replace_ai_content: Whether to replace AI-detected content.
        font_name: Font name to apply (optional).
        text_color: Text color in hex format (optional).
        confidence_threshold: Minimum AI confidence for replacement (0.0-1.0).

    Returns:
        Modified PowerPoint file.
    """
    temp_input = None
    temp_output = None

    try:
        # Read and validate file
        file_content = await file.read()
        validate_pptx_file(file.filename or "unknown.pptx", len(file_content))

        # Save uploaded file
        temp_input = save_uploaded_file(file_content, file.filename or "upload.pptx")

        # Initialize components
        analyzer = PPTAnalyzer()
        modifier = PPTModifier(temp_input)

        # Step 1: Replace AI content if requested
        if replace_ai_content:
            logger.info("Detecting and replacing AI content")

            # Extract text from slides
            slides_text = analyzer.extract_text_from_pptx(temp_input)

            # Detect AI content
            detector = get_detector()
            generator = ContentGenerator()

            replacements = []
            for slide_text in slides_text:
                if not slide_text.text.strip():
                    continue

                detection = detector.detect(slide_text.text)

                # Only replace if confidence exceeds threshold
                if detection.is_ai_generated and detection.confidence >= confidence_threshold:
                    logger.info(
                        f"Replacing AI content in slide {slide_text.slide_number} "
                        f"(confidence: {detection.confidence:.2f})"
                    )

                    # Generate alternative content
                    new_text = generator.generate(slide_text.text)

                    replacements.append(
                        Replacement(
                            slide_num=slide_text.slide_number,
                            old_text=slide_text.text,
                            new_text=new_text,
                        )
                    )

            if replacements:
                modifier.replace_content(replacements)
                logger.info(f"Applied {len(replacements)} content replacements")
            else:
                logger.info("No AI content detected above threshold")

        # Step 2: Apply style changes if requested
        if font_name or text_color:
            logger.info("Applying style modifications")

            color_scheme = None
            if text_color:
                color_scheme = ColorScheme(text_color=text_color)

            style_config = StyleConfig(font_name=font_name, color_scheme=color_scheme)

            modifier.modify_styles(style_config)

        # Step 3: Save modified presentation
        temp_output = generate_temp_filename(".pptx")
        modifier.save(temp_output)

        logger.info(f"Presentation modified successfully: {temp_output}")

        # Return modified file
        return FileResponse(
            temp_output,
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            filename=f"modified_{file.filename or 'presentation.pptx'}",
        )

    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"PPTX modification failed: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        # Cleanup input file (output file will be cleaned up after response is sent)
        if temp_input:
            cleanup_file(temp_input)

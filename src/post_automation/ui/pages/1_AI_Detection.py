"""AI Detection Streamlit page."""

import streamlit as st

from post_automation.core.ai_detector import get_detector
from post_automation.core.ppt_analyzer import PPTAnalyzer
from post_automation.utils.file_handler import cleanup_file, save_uploaded_file
from post_automation.utils.logger import setup_logger

logger = setup_logger(__name__)

st.set_page_config(page_title="AI Detection", page_icon="🔍", layout="wide")

st.title("🔍 AI Content Detection")
st.markdown("---")

# Detection mode selection
detection_mode = st.radio(
    "Choose detection mode:",
    ["Text Input", "PowerPoint File"],
    horizontal=True
)

st.markdown("---")

if detection_mode == "Text Input":
    st.subheader("📝 Text Analysis")

    # Text input
    text_input = st.text_area(
        "Enter text to analyze:",
        height=200,
        placeholder="Paste your text here to check if it's AI-generated..."
    )

    if st.button("🔍 Analyze Text", type="primary", use_container_width=True):
        if text_input and len(text_input.strip()) >= 10:
            with st.spinner("Analyzing text..."):
                try:
                    # Get detector and run analysis
                    detector = get_detector()
                    result = detector.detect(text_input)

                    # Display results
                    st.success("Analysis Complete!")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("Classification", result.label)

                    with col2:
                        st.metric("Confidence", f"{result.confidence:.1%}")

                    with col3:
                        st.metric("Model", result.model_name.split("/")[-1])

                    # Confidence interpretation
                    st.markdown("### 📊 Interpretation")

                    if result.confidence >= 0.8:
                        st.info(
                            f"**High Confidence:** The text is very likely {result.label}-generated.",
                            icon="🎯"
                        )
                    elif result.confidence >= 0.5:
                        st.warning(
                            f"**Medium Confidence:** The text is probably {result.label}-generated.",
                            icon="⚠️"
                        )
                    else:
                        st.error(
                            f"**Low Confidence:** Uncertain classification. More text may be needed.",
                            icon="❓"
                        )

                    # Progress bar for confidence
                    st.progress(result.confidence)

                except Exception as e:
                    st.error(f"Error during analysis: {str(e)}")
                    logger.error(f"Text detection error: {e}")
        else:
            st.warning("Please enter at least 10 characters of text to analyze.")

else:  # PowerPoint File mode
    st.subheader("📊 PowerPoint Analysis")

    uploaded_file = st.file_uploader(
        "Upload PowerPoint file",
        type=["pptx"],
        help="Upload a .pptx file to analyze each slide for AI-generated content"
    )

    if uploaded_file is not None:
        if st.button("🔍 Analyze Presentation", type="primary", use_container_width=True):
            temp_path = None

            with st.spinner("Analyzing presentation..."):
                try:
                    # Save uploaded file
                    file_content = uploaded_file.read()
                    temp_path = save_uploaded_file(file_content, uploaded_file.name)

                    # Extract text from slides
                    analyzer = PPTAnalyzer()
                    slides_text = analyzer.extract_text_from_pptx(temp_path)

                    # Detect AI in each slide
                    detector = get_detector()
                    ai_count = 0
                    slide_results = []

                    for slide_text in slides_text:
                        if slide_text.text.strip():
                            detection = detector.detect(slide_text.text)
                            if detection.is_ai_generated:
                                ai_count += 1
                            slide_results.append({
                                "slide_num": slide_text.slide_number,
                                "text": slide_text.text,
                                "detection": detection
                            })
                        else:
                            slide_results.append({
                                "slide_num": slide_text.slide_number,
                                "text": "(Empty slide)",
                                "detection": None
                            })

                    # Display overall results
                    st.success("Analysis Complete!")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("Total Slides", len(slides_text))

                    with col2:
                        st.metric("AI-Generated", ai_count)

                    with col3:
                        st.metric("Human-Written", len(slides_text) - ai_count)

                    # Display per-slide results
                    st.markdown("### 📄 Slide-by-Slide Results")

                    for result in slide_results:
                        with st.expander(f"Slide {result['slide_num'] + 1}"):
                            if result['detection']:
                                detection = result['detection']

                                # Classification badge
                                if detection.is_ai_generated:
                                    st.markdown(f"**Classification:** 🤖 {detection.label}")
                                else:
                                    st.markdown(f"**Classification:** 👤 {detection.label}")

                                st.markdown(f"**Confidence:** {detection.confidence:.1%}")

                                # Show text preview
                                st.markdown("**Text Preview:**")
                                st.text_area(
                                    "Text",
                                    value=result['text'][:500] + ("..." if len(result['text']) > 500 else ""),
                                    height=100,
                                    disabled=True,
                                    key=f"text_{result['slide_num']}"
                                )

                                # Progress bar
                                st.progress(detection.confidence)
                            else:
                                st.markdown("**Empty slide** - No text to analyze")

                except Exception as e:
                    st.error(f"Error during analysis: {str(e)}")
                    logger.error(f"PPTX detection error: {e}")
                finally:
                    if temp_path:
                        cleanup_file(temp_path)

# Sidebar info
with st.sidebar:
    st.markdown("### ℹ️ About AI Detection")
    st.markdown(
        """
        This tool uses HuggingFace transformer models to detect AI-generated content.

        **How it works:**
        - Analyzes text patterns
        - Compares against AI model signatures
        - Provides confidence scores

        **Confidence Levels:**
        - High (≥80%): Very reliable
        - Medium (50-80%): Fairly reliable
        - Low (<50%): May need more text

        **Best Practices:**
        - Provide at least 50 characters
        - Use complete sentences
        - More text = better accuracy
        """
    )

"""PowerPoint Modification Streamlit page."""

import streamlit as st

from post_automation.core.ai_detector import get_detector
from post_automation.core.content_generator import ContentGenerator
from post_automation.core.ppt_analyzer import PPTAnalyzer
from post_automation.core.ppt_modifier import PPTModifier
from post_automation.models.ppt import ColorScheme, Replacement, StyleConfig
from post_automation.utils.file_handler import cleanup_file, generate_temp_filename, save_uploaded_file
from post_automation.utils.logger import setup_logger

logger = setup_logger(__name__)

st.set_page_config(page_title="PPT Modification", page_icon="📝", layout="wide")

st.title("📝 PowerPoint Modification")
st.markdown("---")

st.markdown(
    """
    Upload a PowerPoint presentation to:
    - Replace AI-detected content with human-like alternatives
    - Apply custom styles and formatting
    - Download the modified presentation
    """
)

st.markdown("---")

# File upload
uploaded_file = st.file_uploader(
    "Upload PowerPoint file",
    type=["pptx"],
    help="Upload a .pptx file to modify"
)

if uploaded_file is not None:
    st.success(f"File uploaded: {uploaded_file.name}")

    # Modification options
    st.subheader("🎨 Modification Options")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Content Replacement")
        replace_ai = st.checkbox(
            "Replace AI-detected content",
            value=True,
            help="Automatically replace text identified as AI-generated"
        )

        if replace_ai:
            confidence_threshold = st.slider(
                "AI Confidence Threshold",
                min_value=0.5,
                max_value=1.0,
                value=0.7,
                step=0.05,
                help="Only replace content if AI confidence is above this threshold"
            )

    with col2:
        st.markdown("#### Style Changes")
        apply_styles = st.checkbox(
            "Apply style changes",
            value=False,
            help="Modify fonts and colors throughout the presentation"
        )

        if apply_styles:
            font_name = st.selectbox(
                "Font",
                ["Arial", "Calibri", "Times New Roman", "Verdana", "Helvetica"],
                index=0
            )

            text_color = st.color_picker(
                "Text Color",
                value="#000000"
            )
        else:
            font_name = None
            text_color = None

    st.markdown("---")

    # Modify button
    if st.button("🚀 Modify Presentation", type="primary", use_container_width=True):
        temp_input = None
        temp_output = None

        with st.spinner("Modifying presentation..."):
            try:
                # Save uploaded file
                file_content = uploaded_file.read()
                temp_input = save_uploaded_file(file_content, uploaded_file.name)

                # Initialize components
                analyzer = PPTAnalyzer()
                modifier = PPTModifier(temp_input)

                progress_bar = st.progress(0)
                status_text = st.empty()

                # Step 1: Replace AI content
                if replace_ai:
                    status_text.text("Detecting AI content...")
                    progress_bar.progress(20)

                    slides_text = analyzer.extract_text_from_pptx(temp_input)
                    detector = get_detector()
                    generator = ContentGenerator()

                    replacements = []
                    for slide_text in slides_text:
                        if not slide_text.text.strip():
                            continue

                        detection = detector.detect(slide_text.text)

                        if detection.is_ai_generated and detection.confidence >= confidence_threshold:
                            new_text = generator.generate(slide_text.text)
                            replacements.append(
                                Replacement(
                                    slide_num=slide_text.slide_number,
                                    old_text=slide_text.text,
                                    new_text=new_text
                                )
                            )

                    if replacements:
                        status_text.text(f"Replacing {len(replacements)} AI-detected slides...")
                        progress_bar.progress(50)
                        modifier.replace_content(replacements)
                        st.info(f"✅ Replaced content in {len(replacements)} slides")
                    else:
                        st.warning("No AI-detected content found above the threshold")

                # Step 2: Apply styles
                if apply_styles:
                    status_text.text("Applying style changes...")
                    progress_bar.progress(70)

                    color_scheme = ColorScheme(text_color=text_color) if text_color else None
                    style_config = StyleConfig(
                        font_name=font_name,
                        color_scheme=color_scheme
                    )

                    modifier.modify_styles(style_config)
                    st.info(f"✅ Applied style changes: Font={font_name}, Color={text_color}")

                # Step 3: Save modified presentation
                status_text.text("Saving modified presentation...")
                progress_bar.progress(90)

                temp_output = generate_temp_filename(".pptx")
                modifier.save(temp_output)

                progress_bar.progress(100)
                status_text.text("✅ Modification complete!")

                # Download button
                with open(temp_output, "rb") as f:
                    modified_content = f.read()

                st.success("Presentation modified successfully!")

                st.download_button(
                    label="📥 Download Modified Presentation",
                    data=modified_content,
                    file_name=f"modified_{uploaded_file.name}",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    use_container_width=True
                )

            except Exception as e:
                st.error(f"Error during modification: {str(e)}")
                logger.error(f"PPT modification error: {e}")
            finally:
                if temp_input:
                    cleanup_file(temp_input)
                if temp_output:
                    cleanup_file(temp_output)

# Sidebar info
with st.sidebar:
    st.markdown("### ℹ️ About PPT Modification")
    st.markdown(
        """
        **Content Replacement:**
        - Detects AI-generated slides
        - Generates human-like alternatives
        - Preserves original formatting

        **Style Changes:**
        - Apply consistent fonts
        - Change text colors
        - Modify formatting

        **Tips:**
        - Higher confidence threshold = fewer replacements
        - Lower confidence threshold = more replacements
        - Preview results before final use

        **Supported:**
        - Text shapes
        - Tables
        - Basic formatting

        **Not Supported:**
        - Images (no OCR)
        - Charts (complex structures)
        - SmartArt
        """
    )

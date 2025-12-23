#!/usr/bin/env python
"""Generate n8n workflow JSON file."""

import argparse

from src.post_automation.workflows.generator import WorkflowGenerator


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="Generate n8n workflow JSON")

    parser.add_argument(
        "--api-url",
        default="http://localhost:8000",
        help="Base URL for the API (default: http://localhost:8000)",
    )

    parser.add_argument(
        "--output",
        default="workflows/workflow.json",
        help="Output file path (default: workflows/workflow.json)",
    )

    parser.add_argument(
        "--confidence",
        type=float,
        default=0.7,
        help="AI confidence threshold (default: 0.7)",
    )

    parser.add_argument(
        "--simple",
        action="store_true",
        help="Generate simple detection-only workflow",
    )

    args = parser.parse_args()

    print(f"🔧 Generating n8n workflow...")
    print(f"   API URL: {args.api_url}")
    print(f"   Output: {args.output}")
    print(f"   Confidence: {args.confidence}")
    print(f"   Type: {'Simple' if args.simple else 'Full'}")
    print()

    generator = WorkflowGenerator(api_base_url=args.api_url)

    if args.simple:
        generator.generate_simple_detection_workflow(output_path=args.output)
    else:
        generator.generate_workflow(
            output_path=args.output, confidence_threshold=args.confidence
        )

    print(f"✅ Workflow generated successfully!")
    print(f"📄 File: {args.output}")
    print()
    print("Next steps:")
    print("1. Import the workflow into n8n")
    print("2. Activate the workflow")
    print("3. Test with webhook trigger")


if __name__ == "__main__":
    main()

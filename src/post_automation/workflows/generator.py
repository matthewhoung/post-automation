"""n8n workflow generator."""

import json
from pathlib import Path
from typing import Optional

from post_automation.utils.logger import setup_logger

logger = setup_logger(__name__)


class WorkflowGenerator:
    """Generator for n8n workflow JSON files."""

    def __init__(self, api_base_url: str = "http://localhost:8000"):
        """
        Initialize workflow generator.

        Args:
            api_base_url: Base URL for the API.
        """
        self.api_base_url = api_base_url
        self.template_path = Path(__file__).parent / "templates" / "base_workflow.json"

    def generate_workflow(
        self, output_path: Optional[str] = None, confidence_threshold: float = 0.7
    ) -> dict:
        """
        Generate n8n workflow from template.

        Args:
            output_path: Path to save workflow JSON. If None, doesn't save to file.
            confidence_threshold: AI confidence threshold for modifications.

        Returns:
            Generated workflow as dictionary.
        """
        logger.info(f"Generating n8n workflow with API base URL: {self.api_base_url}")

        # Load template
        with open(self.template_path, "r") as f:
            workflow = json.load(f)

        # Update API URLs in workflow
        for node in workflow.get("nodes", []):
            if node.get("type") == "n8n-nodes-base.httpRequest":
                params = node.get("parameters", {})
                if "url" in params:
                    # Replace environment variable with actual URL
                    url = params["url"]
                    url = url.replace("={{$env.API_BASE_URL}}", self.api_base_url)
                    params["url"] = url

                # Update confidence threshold if applicable
                if "modify" in node.get("name", "").lower():
                    options = params.get("options", {})
                    query_params = options.get("queryParameters", {})
                    params_list = query_params.get("parameters", [])

                    for param in params_list:
                        if param.get("name") == "confidence_threshold":
                            param["value"] = str(confidence_threshold)

        # Save to file if path provided
        if output_path:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, "w") as f:
                json.dump(workflow, f, indent=2)

            logger.info(f"Workflow saved to: {output_path}")

        return workflow

    def generate_simple_detection_workflow(self, output_path: Optional[str] = None) -> dict:
        """
        Generate a simple workflow that only detects AI content.

        Args:
            output_path: Path to save workflow JSON.

        Returns:
            Generated workflow as dictionary.
        """
        workflow = {
            "name": "Simple AI Detection",
            "nodes": [
                {
                    "parameters": {"path": "detect-ai", "responseMode": "responseNode"},
                    "id": "webhook",
                    "name": "Webhook",
                    "type": "n8n-nodes-base.webhook",
                    "typeVersion": 1,
                    "position": [250, 300],
                },
                {
                    "parameters": {
                        "method": "POST",
                        "url": f"{self.api_base_url}/api/detect/text",
                        "sendBody": true,
                        "specifyBody": "json",
                        "jsonBody": '={{ {"text": $json.text} }}',
                    },
                    "id": "detect",
                    "name": "Detect AI",
                    "type": "n8n-nodes-base.httpRequest",
                    "typeVersion": 3,
                    "position": [450, 300],
                },
                {
                    "parameters": {"respondWith": "allIncomingItems"},
                    "id": "respond",
                    "name": "Respond",
                    "type": "n8n-nodes-base.respondToWebhook",
                    "typeVersion": 1,
                    "position": [650, 300],
                },
            ],
            "connections": {
                "Webhook": {"main": [[{"node": "Detect AI", "type": "main", "index": 0}]]},
                "Detect AI": {"main": [[{"node": "Respond", "type": "main", "index": 0}]]},
            },
            "active": false,
            "settings": {},
        }

        if output_path:
            with open(output_path, "w") as f:
                json.dump(workflow, f, indent=2)
            logger.info(f"Simple workflow saved to: {output_path}")

        return workflow


def generate_workflow_cli(
    api_url: str = "http://localhost:8000",
    output: str = "workflows/workflow.json",
    confidence: float = 0.7,
):
    """
    CLI function to generate workflow.

    Args:
        api_url: Base URL for the API.
        output: Output file path.
        confidence: AI confidence threshold.
    """
    generator = WorkflowGenerator(api_base_url=api_url)
    generator.generate_workflow(output_path=output, confidence_threshold=confidence)
    print(f"✅ Workflow generated successfully: {output}")


if __name__ == "__main__":
    import sys

    # Simple CLI
    api_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    output = sys.argv[2] if len(sys.argv) > 2 else "workflows/workflow.json"
    confidence = float(sys.argv[3]) if len(sys.argv) > 3 else 0.7

    generate_workflow_cli(api_url, output, confidence)

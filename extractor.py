from pathlib import Path
import json

from schema import Consultation

template = Path("prompts/extract_v1.txt").read_text()
examples = Path("few_shot_examples.txt").read_text()

def render_prompt(document: str) -> str:
    return template.format(
        domain="healthcare data extraction engine",
        schema=json.dumps(Consultation.model_json_schema(),
                        indent=2
        ),
        examples=examples,
        document=document,
    )
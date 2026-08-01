from pathlib import Path
import json
import anthropic 
from config import API_KEY, BASE_URL, MODEL
from pydantic import ValidationError

from schema import Consultation

template = Path("prompts/extract_v2.txt").read_text(encoding="utf-8")
examples = Path("few_shot_examples.txt").read_text(encoding="utf-8")

def render_prompt(document: str) -> str:
    return template.format(
        domain="healthcare data extraction engine",
        schema=json.dumps(Consultation.model_json_schema(),
                        indent=2
        ),
        examples=examples,
        document=document,
    )
    
client = anthropic.Anthropic(api_key=API_KEY, base_url=BASE_URL)
    
def call_llm(messages: list[dict], temperature: float = 0) -> str:
    response = client.messages.create(
        model = MODEL,
        max_tokens = 500,
        messages=messages,
        temperature=temperature
    ) 
    return response.content[0].text

def extract(doc: str, retries: int = 2) -> Consultation:
    if not doc.strip():
        return None
    msgs = [
        {
            "role": "user", 
            "content": render_prompt(doc)
        }
    ]
    for attempt in range(retries + 1):
        raw = call_llm(msgs, temperature=0)
        try:
            return Consultation.model_validate_json(raw)
        except ValidationError as e:
            msgs += [{"role": "assistant", 
                      "content": raw},
                     {"role": "user", 
                      "content": f"Your JSON failed validation:\n{e}\n"
                      "Return corrected JSON only."}]
    raise RuntimeError(f"Extraction failed after {retries+1} tries")


# document = Path("golden/doc01.txt").read_text(encoding="utf-8")

# result = extract(document)

# print(result.model_dump_json(indent=2))
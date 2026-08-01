# field-level accuracy across the golden set
from extractor import extract
import json
from glob import glob
from pathlib import Path

passed = 0
total_scored = 0

for doc_path in sorted(glob("golden/doc[0-9][0-9].txt")):
    document = Path(doc_path).read_text(encoding="utf-8")
    expected_path = doc_path.replace(".txt", ".expected.json")
    try:
        result = extract(document)
    except RuntimeError as e:
        print(doc_path, f"Failed: {e}")
        continue
    
    if result is None:
        print(doc_path, "Failed. Empty or malformed document.")
        continue
    
    if not Path(expected_path).exists():
        print(doc_path, "Skipped. No expected JSON.")
        continue
    
    with open(expected_path, encoding="utf-8") as f:
        expected = json.load(f)
        
    got = result.model_dump()
    # for k, v in expected.items():
    #     if got.get(k) != v:
    #         print("Mismatch:", k)
    #         print("Expected:", v)
    #         print("Got:", got.get(k))

    fields_ok = sum(got.get(k) == v for k, v in expected.items())
    total_fields = len(expected)
    
    print(doc_path, f"{fields_ok}/{len(expected)} fields")
    
    total_scored += 1
    if fields_ok == total_fields:
        passed += 1

print(f"\n{passed}/{total_scored} documents fully passed")
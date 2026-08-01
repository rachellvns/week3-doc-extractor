# field-level accuracy across the golden set
from extractor import extract
import json
from glob import glob

for doc_path in sorted(glob("golden/doc*.txt")):
    expected = json.load(open(doc_path.replace(".txt", 
                                               ".expected.json")))
    got = extract(open(doc_path).read()).model_dump()
    fields_ok = sum(got.get(k) == v for k, v in expected.items())
    print(doc_path, f"{fields_ok}/{len(expected)} fields")
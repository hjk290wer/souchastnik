#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "app" / "src" / "main" / "assets"

def main():
    articles = json.loads((ASSETS / "articles.json").read_text(encoding="utf-8"))
    triggers = json.loads((ASSETS / "triggers.json").read_text(encoding="utf-8"))
    codes = [a["code"] for a in articles["articles"]]
    code_set = set(codes)
    labels = [a["label"] for a in articles["articles"]]
    errors = []
    if len(codes) != len(code_set):
        errors.append("duplicate article codes")
    if len(labels) != len(set(labels)):
        errors.append("duplicate article labels")
    if articles.get("_none_label") in set(labels):
        errors.append("_none_label collides with article label")
    referenced = set()
    for i, group in enumerate(triggers.get("groups", []), 1):
        if not group.get("words"):
            errors.append(f"group {i}: empty words")
        if not group.get("codes"):
            errors.append(f"group {i}: empty codes")
        if not group.get("clean"):
            errors.append(f"group {i}: missing clean")
        for code in group.get("codes", []):
            referenced.add(code)
            if code not in code_set:
                errors.append(f"group {i}: unknown code {code}")
    for code in sorted(code_set - referenced):
        errors.append(f"unreachable article {code}")
    print(f"articles={len(codes)} trigger_groups={len(triggers.get('groups', []))} covered={len(referenced)}")
    if errors:
        print("FAILED")
        for error in errors:
            print(" -", error)
        return 1
    print("PASSED")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

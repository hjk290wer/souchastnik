#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "app" / "src" / "main" / "assets"
EXPECTED_ARTICLES = 80
EXPECTED_VERSION = "0.2-test"

def load(name):
    return json.loads((ASSETS / name).read_text(encoding="utf-8"))

def main():
    articles = load("articles.json")
    triggers = load("triggers.json")
    agents = load("agents.json")
    arts = articles.get("articles", [])
    codes = [a["code"] for a in arts]
    labels = [a["label"] for a in arts]
    errors = []
    if len(arts) != EXPECTED_ARTICLES:
        errors.append(f"article count changed: expected {EXPECTED_ARTICLES}, got {len(arts)}")
    if articles.get("_version") != EXPECTED_VERSION:
        errors.append(f"unexpected corpus version: expected {EXPECTED_VERSION}, got {articles.get('_version')}")
    if len(codes) != len(set(codes)):
        errors.append("duplicate article codes")
    if len(labels) != len(set(labels)):
        errors.append("duplicate article labels")
    if articles.get("_none_label") in set(labels):
        errors.append("_none_label collides with article label")
    for i, article in enumerate(arts, 1):
        if not isinstance(article.get("penalty"), str) or not article["penalty"].strip():
            errors.append(f"article {i}: missing penalty")
    code_set = set(codes)
    referenced = set()
    for i, group in enumerate(triggers.get("groups", []), 1):
        words = group.get("words", [])
        refs = group.get("codes", [])
        if not words:
            errors.append(f"group {i}: empty words")
        if not refs:
            errors.append(f"group {i}: empty codes")
        if not group.get("clean"):
            errors.append(f"group {i}: missing clean")
        for code in refs:
            referenced.add(code)
            if code not in code_set:
                errors.append(f"group {i}: unknown code {code}")
    for code in sorted(code_set - referenced):
        errors.append(f"unreachable article {code}")
    templates = agents.get("templates", {})
    for section in ("agents", "services"):
        for i, entry in enumerate(agents.get(section, []), 1):
            kind = entry.get("kind", "agent")
            if kind not in templates:
                errors.append(f"{section}[{i}]: missing template for kind={kind}")
            if not entry.get("forms") and not entry.get("exact"):
                errors.append(f"{section}[{i}]: no forms/exact")
            if not entry.get("name"):
                errors.append(f"{section}[{i}]: missing name")
    print(f"articles={len(arts)} trigger_groups={len(triggers.get('groups', []))} covered={len(referenced)}")
    print(f"agents={len(agents.get('agents', []))} services={len(agents.get('services', []))}")
    if errors:
        print("FAILED")
        for e in errors:
            print(" -", e)
        return 1
    print("PASSED")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

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
    a = load("articles.json")
    t = load("triggers.json")
    codes = {x["code"] for x in a["articles"]}
    refs = {c for g in t["groups"] for c in g["codes"]}
    unknown = sorted(refs - codes)
    missing = sorted(codes - refs)
    print(f"articles={len(a['articles'])} refs={len(refs)} unknown={len(unknown)} missing={len(missing)}")
    if len(a["articles"]) != EXPECTED_ARTICLES or a.get("_version") != EXPECTED_VERSION or unknown or missing:
        print("FAILED")
        return 1
    print("PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

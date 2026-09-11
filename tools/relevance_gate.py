#!/usr/bin/env python3
"""Review gate for internet-relevant criminal-law articles.

The app is a text classifier, not a general criminal-code encyclopedia. An
article belongs in articles.json only when a post/message/comment/file/link or
other online action can itself be a material way of committing the offence,
or when publication is an explicit qualifying circumstance.

This script intentionally errs on the side of exclusion: entries require an
explicit rationale field in the review manifest before they are admitted.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "app" / "src" / "main" / "assets"


def main() -> int:
    articles = json.loads((ASSETS / "articles.json").read_text(encoding="utf-8"))["articles"]
    for article in articles:
        if not article.get("internet"):
            raise SystemExit(f"article {article['code']} has no internet relevance flag")
        if not article.get("rationale"):
            raise SystemExit(f"article {article['code']} has no rationale")
    print(f"PASSED: {len(articles)} articles have explicit internet relevance rationale")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

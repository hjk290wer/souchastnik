#!/usr/bin/env python3
"""Review gate for internet-relevant criminal-law articles.

The app is a text classifier, not a general criminal-code encyclopedia. An
article belongs in articles.json only when a post/message/comment/file/link or
other online action can itself be a material way of committing the offence,
or when publication is an explicit qualifying circumstance.

This gate accepts the locked first-test corpus. Articles are still required to
carry an explicit internet flag and rationale so the scope remains auditable.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "app" / "src" / "main" / "assets"
EXPECTED_ARTICLES = 80


def main() -> int:
    data = json.loads((ASSETS / "articles.json").read_text(encoding="utf-8"))
    articles = data["articles"]
    if len(articles) != EXPECTED_ARTICLES:
        raise SystemExit(f"expected {EXPECTED_ARTICLES} articles, got {len(articles)}")

    missing = []
    for article in articles:
        if not article.get("internet"):
            missing.append(f"article {article['code']} has no internet relevance flag")
        if not article.get("rationale"):
            missing.append(f"article {article['code']} has no rationale")

    if missing:
        raise SystemExit("\n".join(missing))

    print(f"PASSED: {len(articles)} articles have explicit internet relevance rationale")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

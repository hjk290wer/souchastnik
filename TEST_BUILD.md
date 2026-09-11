# First test build

## Corpus lock

The current test corpus is intentionally frozen at **80 articles**.

- Version: `0.2-test`
- Article count: `80`
- Purpose: first APK/runtime test before expanding the corpus to 100 internet-relevant articles.

## Classification policy

A trigger is never a verdict. Triggers only narrow the candidate set.

The judge must interpret the full text and distinguish at least:

- assertion vs. quotation;
- statement vs. question;
- endorsement vs. refutation;
- author's own words vs. report about another person;
- public dissemination vs. private communication;
- factual statement vs. opinion/sarcasm/fiction/history/education;
- required special subject and qualifying circumstances.

The result must explain why a candidate was selected or rejected.

## Penalty display policy

Every displayed article must include the **minimum applicable punishment** and the **maximum applicable punishment** available from the stored sanction data. For alternative sanctions, show the least severe available punishment explicitly instead of inventing a prison term.

## Build

GitHub Actions workflow `Test build` runs:

1. dictionary validation;
2. internet-scope validation;
3. Android debug build with Gradle 8.9 and Java 17;
4. APK upload as workflow artifact.

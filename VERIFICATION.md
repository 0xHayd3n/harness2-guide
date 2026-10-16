# Verification record

[Overview](README.md) · [Sources](SOURCES.md)

Prepared October 16, 2026 for arXiv:2610.14224v1. These checks concern the reading guide's source fidelity and publication quality; they do not validate the research or reproduce its experiments.

## Source and factual review

- Read all 37 pages, including references, Appendices A–H, and shared/differential prompt blocks.
- Rendered all pages and inspected the figures and tables; cross-checked dense layouts against page images where extracted text was ambiguous.
- Independently reviewed main-table transcriptions, benchmark denominators, recursion semantics, library tests, appendices, failure cases, and author metadata. A separate full-paper reviewer supplied additional factual QA.
- Preserved the default-editor/same-model distinction, baseline exceptions, selection limits, retrospective reuse qualification, nonadditive removal ablations, and Figure 12/Table 1 baseline differences.
- Verified the official implementation and project links, arXiv v1/version history/license link, and recorded upstream release commit and documentation discrepancies.
- Kept the PDF, extracted paper text, page images, private attachment identifiers, transfer records, and local review artifacts outside the public repository.

The official PDF fallback is pinned by size and SHA-256 in [SOURCES.md](SOURCES.md). Attachment byte equivalence remains unverified because supported materialization failed on Windows. No later paper version was listed at the time of checking.

## Automated documentation checks

Run the offline, dependency-free checker from the repository root:

```bash
python scripts/check_docs.py
```

It checks exact publication scope, UTF-8/control characters, local Markdown links and GitHub-style heading anchors, balanced fences, PDF page bounds, source pins, JSON metadata/evidence consistency, selected numeric invariants and derived arithmetic, citation fields, and patterns for private identifiers or credentials. These checks cannot establish scientific validity or detect every prose transcription error. External links and the CFF schema are preparation checks rather than network-dependent CI requirements.

GitHub Actions runs the same checker on pushes and pull requests with read-only contents permissions. Publication and final CI results are recorded after the remote checks complete.

Preparation checks on October 16, 2026 passed: all 24 intended files; structured table/derived-summary consistency; all 19 evidence-indexed claims and eight source records; the official CFF 1.2.0 JSON schema using YAML parsing and JSON Schema validation; and unauthenticated HTTP GET checks returning 200 for all 13 distinct external documentation URLs. The checker was also exercised with deliberately broken arithmetic, fabricated k = 5 uncertainty, wrong paper titles, unpinned PDFs, invalid pages, private-source patterns, and unexpected files to verify that those defects are rejected.

## Limits

No benchmark or model runs were performed. No experiment results, p-values, confidence intervals, latency measurements, or reproduction logs were invented. The structured results are attributed transcriptions and labeled arithmetic, not new observations. The guide is pinned to a paper version, while upstream websites and release defaults can change. Checks of public accessibility show that the repository can be read without authentication; they do not guarantee future availability.

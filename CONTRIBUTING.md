# Contributing

Corrections that improve source fidelity, navigation, or clarity are welcome. Keep this an independent guide to arXiv:2610.14224v1.

For a factual correction, give the exact paper section, figure/table/prompt, PDF page, and version. Explain whether the change corrects a transcription, interpretation, source discrepancy, or derived value. Update the prose and relevant structured metadata together. Keep reported observations distinct from guide interpretation and future-study proposals.

Do not add unsourced benchmark results, copied paper pages, private attachments, credentials, or full upstream source trees. A successful documentation check is not an experimental reproduction. New experiments require their own protocol, artifacts, attribution, and clear separation from authors' reported values.

Before submitting, run:

```bash
python scripts/check_docs.py
```

Review [AGENTS.md](AGENTS.md), [SOURCES.md](SOURCES.md), and [VERIFICATION.md](VERIFICATION.md). Check table values visually in the v1 PDF when extraction is ambiguous. Keep document navigation and the exact publication allowlist synchronized with any added or renamed file. Contributions use the relevant [documentation](LICENSE.md) or [checker](scripts/LICENSE) license.

# Sources and provenance

[Overview](README.md) · [Verification](VERIFICATION.md) · [Attribution](ATTRIBUTION.md)

## Pinned paper

| Field | Record |
| --- | --- |
| Title | Harness²: Recursive Agent Harnessing for an Open World |
| Identifier | arXiv:2610.14224v1 |
| Abstract | https://arxiv.org/abs/2610.14224v1 |
| PDF used | https://arxiv.org/pdf/2610.14224v1 |
| Pages | 37 |
| Retrieved | October 16, 2026 (UTC) |
| Bytes | 8,101,889 |
| SHA-256 | `440be1f694f3b0fdfb8e612e9b2288ff0d8ab38641cfd1064fd77052ba360282` |
| arXiv submission | October 9, 2026, 18:34:25 UTC |
| PDF header | October 12, 2026 |
| Version history | Only v1 listed when checked October 16, 2026 |
| License shown on abstract page | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

The user supplied an attachment named `2610.14224v1.pdf`, described as 8,101,889 bytes and 37 pages. The supported Library transfer reached a Windows metadata operation that failed because Python's `os.setxattr` was unavailable. The attachment was not successfully materialized through that supported route. We used the official version-pinned arXiv PDF instead, without bypassing the Library metadata requirement.

The downloaded official PDF has the supplied filename's version, stated title, author sequence, page count, and byte count. **Byte equivalence with the attachment has not been verified**; matching size and metadata do not establish it. The hash above identifies the actual official PDF read for this guide. No attachment identifiers, transfer URLs, or downloaded source files are published.

The submission date and PDF header differ. We preserve both rather than inferring a second version. The DOI displayed by arXiv is `10.48550/arXiv.2610.14224`; the abstract page labeled its registration pending when checked. The version-pinned arXiv links are the primary citation targets here.

## Source hierarchy

1. **Paper v1:** authority for method, protocol, results, figure/table numbers, stage prompts, and paper-described limitations.
2. **arXiv abstract and history:** authority for identifier, author metadata, submission/version history, and paper license link.
3. **Authors' code at a recorded commit:** authority for the release's own instructions and defaults, not a substitute for v1's experimental description.
4. **Authors' project page:** a useful entry point, not the numerical source for this guide.
5. **This guide:** original explanations, derived arithmetic, diagrams, interpretations, and planning suggestions, labeled accordingly.

The whole PDF was extracted page by page and read, including references and appendices. All pages were rendered for visual inspection, and figure/table content was cross-checked against page images during factual review. Extracted text can corrupt superscripts, arrows, table layout, and mathematical symbols; rendered pages resolve those cases. The public repository contains neither full text extraction nor paper page images.

## Verified author resources

| Resource | Observation on October 16, 2026 |
| --- | --- |
| [Authors' repository](https://github.com/google-research/harness2) | Public, default branch `main`; recorded head `1cfe254e8d25b15f37048c3730134686abe60335` |
| [Pinned README](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md) | Describes installation, deterministic demo, benchmarks, recursion modes, and web-access caveats |
| [Pinned license](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/LICENSE) | Apache License 2.0 for the implementation; third-party notices apply separately |
| [Project site](https://harness2.github.io/) | HTTP retrieval succeeded; returned HTML title identifies Harness² and the paper. One web retrieval tool could not load it; that alone was not treated as site failure. |

## Paper and release differences

The following compares v1 with the authors' release at the recorded commit. It does not claim that release-validation behavior occurred in the paper's experiments.

| Topic | Paper v1 | Recorded public release |
| --- | --- | --- |
| Evidence isolation | Benchmark answers/rubrics/verdicts are withheld from the pipeline; improvement workspace guard rejects grader material (Appendices B and D.2, pp. 19–21) | [Experiment notes](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/EXPERIMENTS.md) say executor network is unrestricted and Codex sandbox disabled. They report a release-validation JobBench rollout downloading its public rubric. |
| LAB population | 1,251 tasks overall; 100 held-out test tasks evaluated; a separate 24-task development set used by Meta-Harness (pp. 19–20) | Experiment notes describe 1,143 tasks in the full installed LAB stream. This guide does not reconcile the difference by speculation. |
| Task partitions | Frozen benchmark-specific test sets; WorkBuddy 40/35/25, JobBench 34, LAB 100 (pp. 18–20) | Experiment notes describe locally generated domain-stratified partitions with default train fraction 0.5, not released partition assets. They do not establish identity with the paper's task sets. |
| Evaluation failure | One failure case counts each unparsed judge verdict as a failure (Figure 14, p. 26) | [Benchmark notes](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/BENCHMARKS.md) and experiment notes say failed evaluations remain unscored instead of zero. |

These observations matter for reproduction planning. They neither invalidate the reported results by themselves nor establish an exact executable match to them. No release benchmark commands were run here. See [discussion and reproduction planning](docs/06-discussion-and-reproduction.md).

## Internal paper differences

- Figure 12's cross-model analysis uses a GLM-5 Code base of 58.5 and Office base of 73.7. Table 1's corresponding OpenCode base row is 58.4 and 75.1. Keep these source-specific analyses separate; the guide does not invent a reason for the difference. [Table 1, p. 8](https://arxiv.org/pdf/2610.14224v1#page=8), [Figure 12, p. 24](https://arxiv.org/pdf/2610.14224v1#page=24).
- Prompt-scoped invariant/domain roles emphasize different responsibilities, but shared instructions overlap. They are not mechanically disjoint edit permissions. [Appendix H, pp. 30–33](https://arxiv.org/pdf/2610.14224v1#page=30).
- Values derived for k = 5 add displayed, rounded means and displayed deltas. They are marked derived; the source does not supply their standard deviations.

## Version policy

New versions must be reviewed explicitly. Do not silently replace the source hash, combine values from different versions, or update this guide's v1 claims from the moving project site. Record changed claims and preserve version-specific citations. An unchanged arXiv identifier without `v1` can resolve to a later paper in future.

Machine-readable records: [paper](metadata/paper.json), [sources](metadata/sources.json), [claims](metadata/claims.json), [results](data/reported-results.json).

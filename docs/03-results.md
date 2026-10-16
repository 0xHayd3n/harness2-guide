# 3. Results and evaluation

[Previous: Method](02-method.md) · [Overview](../README.md) · [Next: Critical reading](04-critical-reading.md)

[Machine-readable reported results](../data/reported-results.json)

All numbers here come from **arXiv:2610.14224v1**, not experiments run for this repository. Page references below refer to the 37-page pinned PDF; its printed page numbers match PDF page numbers. Calculated totals are labeled **derived**.

- [What was evaluated](#what-was-evaluated)
- [How to read the main tables](#how-to-read-the-main-tables)
- [Main results](#main-results)
- [What the baselines compare](#what-the-baselines-compare)
- [Reading Figures 1 and 4-7](#reading-figures-1-and-4-7)
- [Ablations](#ablations)
- [Supplementary evidence](#supplementary-evidence)
- [Limits on the conclusions](#limits-on-the-conclusions)
- [Data notes](#data-notes)

## What was evaluated

The main evaluation crosses two frozen executors, **Gemini 3.5 Flash** and **GLM-5**, with two initial agent harnesses, **OpenCode** and **Codex**. The default improver is **Claude Opus 4.8 under OpenCode at high reasoning effort**. The paper reports three independent streams with shuffled task order. Every benchmark's stream begins with an empty improvement library; library directories are domain-specific. Future tasks are unavailable during the online stream, and completed tasks are not replayed. Each new task starts from the common initial execution harness, with earlier harnesses and lessons available for selective reuse through the improver. [Sections 2.1-2.3 and 3.1, pp. 4-7; Appendices A-D, pp. 18-21.](https://arxiv.org/pdf/2610.14224v1#page=4)

| Benchmark | Evaluation tasks | Reported score | Evaluation machinery |
| --- | --- | --- | --- |
| WorkBuddy-Bench | Code 40, Web 35, Office 25; test halves of 80/70/50 tasks, split by category | Fraction of a task's checks passed, displayed on a 0-100 scale; the headline Avg. gives each domain equal weight | Deterministic hidden tests and file/structure checks plus LLM/VLM items; Gemini 3.5 Flash judges where needed |
| JobBench | 34 held-out tasks from a frozen 31/34 split of 65 tasks across seven occupational domains | Weighted rubric score divided by maximum, displayed on a 0-100 scale | Claude Opus 4.8 |
| LAB | A stratified 100-task held-out subset of 1,251 legal tasks across 24 practice areas and four work types | **Partial**: percentage of grading criteria passed | Claude Sonnet 4.6; no executable correctness check |

The 24-task LAB development set is used only by Meta-Harness. The benchmark's hidden checks, rubric, expected values, and grading scores are evaluation resources: the paper says they are withheld from the executor, editor, and selector. Thus **label-free improvement does not mean evaluation without labels or judges**. LAB's Partial is criterion-based; the paper does not specify the total criterion denominator for its 100-task evaluation subset, so a pass rate cannot be converted into a count of passed criteria from the task count alone. [Appendix B, pp. 18-20.](https://arxiv.org/pdf/2610.14224v1#page=18)

The stock harness is extended with benchmark reference instructions; its always-on files are otherwise empty and on-demand directories initially contain placeholders. This is the paper's stated starting configuration, not a guarantee that any later release of an off-the-shelf agent has the same defaults. Rollouts are capped at 200 model turns and 3,600 seconds. Each WorkBuddy rollout uses a fresh container, with the benchmark timeout set to twice its default. Invalid harness proposals are retried once with validation feedback; a second failure inherits the incoming tree and records the fallback. [Appendix D.1-D.2, p. 21.](https://arxiv.org/pdf/2610.14224v1#page=21)

## How to read the main tables

**Tables 1 and 2 report one improvement step at `k=1`.** Values in parentheses are standard deviations over three runs, not confidence intervals. Their blue **+ Recursion** rows are **changes in means** when using parallel task-level recursion at `k=5`; they are neither absolute scores nor standard deviations. At `k=1`, the selector is bypassed. At `k>1`, it chooses an already executed deliverable without seeing the originating harness or a grading score. [Section 2.2 and Tables 1-2, pp. 5-9.](https://arxiv.org/pdf/2610.14224v1#page=5)

WorkBuddy's Avg. is the **macro-average of its three domain scores**, with SD calculated over per-run averages. The unequal task counts mean this is different from pooling all 100 test tasks. Averaging the three domain SDs would also be incorrect. [Table 1, p. 8.](https://arxiv.org/pdf/2610.14224v1#page=8)

**#Steps counts model turns in the executor's session.** It is useful for understanding execution behavior, but cannot substitute for the full cost of reference rollouts, candidate probes, editor/composer sessions, and selection. Figure 6 provides the separate total-token comparison. [Appendix B, p. 20; Figure 6, p. 10.](https://arxiv.org/pdf/2610.14224v1#page=20)

## Main results

In the next three tables, `mean ± SD` is copied from the paper. **One-step gain** is a subtraction of displayed means. **Extra at k=5** is copied from the recursion row. **k=5 total** is derived by adding that delta to the displayed one-step mean; the paper does not provide its SD.

### WorkBuddy-Bench: three-domain macro-average

| Executor / initial harness | Base | Harness2 k=1 | One-step gain | Extra at k=5 | k=5 total, derived |
| --- | ---: | ---: | ---: | ---: | ---: |
| Gemini 3.5 Flash / OpenCode | 72.4 ± 0.9 | 77.5 ± 2.5 | +5.1 | +3.3 | 80.8 |
| Gemini 3.5 Flash / Codex | 74.5 ± 1.6 | 77.5 ± 2.0 | +3.0 | +2.9 | 80.4 |
| GLM-5 / OpenCode | 64.2 ± 1.4 | 75.7 ± 2.2 | +11.5 | +3.9 | 79.6 |
| GLM-5 / Codex | 64.4 ± 1.2 | 75.3 ± 1.3 | +10.9 | +3.0 | 78.3 |

Units: score points on the paper's 0-100 display. Source: [Table 1, p. 8.](https://arxiv.org/pdf/2610.14224v1#page=8)

### JobBench: normalized weighted score

| Executor / initial harness | Base | Harness2 k=1 | One-step gain | Extra at k=5 | k=5 total, derived |
| --- | ---: | ---: | ---: | ---: | ---: |
| Gemini 3.5 Flash / OpenCode | 31.5 ± 1.1 | 36.0 ± 2.3 | +4.5 | +3.0 | 39.0 |
| Gemini 3.5 Flash / Codex | 33.9 ± 2.6 | 35.3 ± 3.5 | +1.4 | +4.2 | 39.5 |
| GLM-5 / OpenCode | 20.6 ± 2.0 | 24.2 ± 0.9 | +3.6 | +4.2 | 28.4 |
| GLM-5 / Codex | 23.6 ± 2.3 | 24.8 ± 0.2 | +1.2 | +3.1 | 27.9 |

Units: score points on the paper's 0-100 display. Source: [Table 2, p. 9.](https://arxiv.org/pdf/2610.14224v1#page=9)

### LAB: criterion pass rate

| Executor / initial harness | Base Partial (%) | Harness2 k=1 (%) | One-step gain (pp) | Extra at k=5 (pp) | k=5 total (%), derived |
| --- | ---: | ---: | ---: | ---: | ---: |
| Gemini 3.5 Flash / OpenCode | 79.9 ± 0.6 | 81.9 ± 0.6 | +2.0 | +2.6 | 84.5 |
| Gemini 3.5 Flash / Codex | 71.6 ± 1.3 | 75.6 ± 4.5 | +4.0 | +2.9 | 78.5 |
| GLM-5 / OpenCode | 59.6 ± 2.7 | 71.4 ± 2.9 | +11.8 | +6.7 | 78.1 |
| GLM-5 / Codex | 58.1 ± 2.3 | 65.9 ± 2.7 | +7.8 | +4.8 | 70.7 |

Here **pp** means percentage points, not relative percent improvement. Source: [Table 2, p. 9.](https://arxiv.org/pdf/2610.14224v1#page=9)

These results support three bounded observations:

- One step beats the corresponding base on all **12 benchmark/configuration pairs**, using WorkBuddy Avg., JobBench Score, and LAB Partial.
- One step beats the compared baselines on WorkBuddy Avg. and JobBench Score in all four configurations. **LAB has an exception:** with Gemini/Codex, Meta-Harness reports 76.5 versus Harness2's 75.6.
- Aggregate wins do not imply every domain wins. With GLM-5/Codex, Meta-Harness scores **76.8 on WorkBuddy Code versus Harness2's 74.9**, even though Harness2's three-domain Avg. is higher.

The headline maximum gains of **11.5 WorkBuddy points, 4.5 JobBench points, and 11.8 LAB percentage points** occur in different configurations. They are not three measurements of one universally best setting. [Section 3.2 and Tables 1-2, pp. 8-9.](https://arxiv.org/pdf/2610.14224v1#page=8)

Executor step counts do not all fall with higher scores. For Gemini/OpenCode, one-step Harness2 reduces WorkBuddy Avg. steps from **25.4 to 21.9**, while increasing JobBench steps from **63.6 to 69.3** and LAB steps from **29.0 to 33.0**. The result is better judged deliverables under these conditions, rather than a claim that refinement always shortens execution. [Tables 1-2, pp. 8-9.](https://arxiv.org/pdf/2610.14224v1#page=8)

## What the baselines compare

All experimental baselines share the frozen executor, initial harness, test stream, and evaluation judge for a configuration. Revision and reflection use Claude Opus 4.8. Their access to preparation data and persistent state differs. [Appendix C, p. 20.](https://arxiv.org/pdf/2610.14224v1#page=20)

| Method | What changes or persists | Preparation / selection details |
| --- | --- | --- |
| Base harness | No harness adaptation | Runs the initial configuration |
| Best-of-k base | Independent base rollouts; no harness edit | The same score-blind selector chooses a deliverable; plotted in Figure 5 |
| ReasoningBank | Fixed harness; strategy memory is retrieved into the task context | At most three items from the most similar past task in the same domain, using `gemini-embedding-001`; success/failure labels come from a self-judge without answers. At larger k, uses memory-aware rollouts, best-of-k selection, and contrastive distillation |
| Harness Scaling | Per-task revision of the same editable components; no cross-task library | Base rollout plus k revision iterations; sees trajectories but no score; final revised tree is deployed, with the base output as fallback if deployment produces none |
| Meta-Harness | Offline search; selected harness stays fixed on test tasks | Labeled search on WorkBuddy/JobBench training tasks or LAB's 24 dev tasks; 10 iterations, two candidates each, three replicates per task, acceptance margin 0.01 |
| Harness2 | Task-local scoped edits and composition, plus a library updated after tasks | No correctness labels during improvement; library starts empty; main comparisons distinguish k=1 from parallel k=5 |

Thus Meta-Harness is a useful strong comparator with a **different preparation protocol**, rather than an identically informed online baseline. A common k also does not establish equal token cost across methods; consult Figure 6 for the measured compute comparison.

**Table 4 is a literature taxonomy, not a benchmark leaderboard.** Its six axes describe the object changed, offline/online stage, external correctness labels, one-pass task/batch streaming, an explicit test-time scaling study, and persistent changes to editing guidance or editor parameters. In particular, the paper's “Improver Update” check does not certify improved improvement ability. Streaming can include batches; a continuous episode by itself does not establish that protocol. The guide's JSON preserves the authors' 28-row categorization without claiming an independent audit of every cited system. [Appendix A.1 and Table 4, pp. 17-19.](https://arxiv.org/pdf/2610.14224v1#page=17)

## Reading Figures 1 and 4-7

### Figure 1: the cover result uses parallel k=5

For Gemini 3.5 Flash/OpenCode, the plotted WorkBuddy scores are **80.8 Code, 78.3 Web, and 83.4 Office**, with gains over base of **7.4, 8.4, and 9.4 points**. These are parallel-recursion results, rather than the one-step values from the main table's Harness2 row. The right panel shows Code's improvement across the studied budget range. [Figure 1, p. 1.](https://arxiv.org/pdf/2610.14224v1#page=1)

### Figure 4: k describes the search organization

This is a method diagram. Parallel recursion uses **k reference executions, k candidates per scope, and k composition sessions**, each receiving the candidate pool. It performs one population update: larger k widens exploration. Sequential recursion chains **k contrastive steps** and accumulates evidence. Neither definition makes k the total number of executor rollouts or a token budget. At k=1 both reduce to the basic step. [Section 2.2.2 and Figure 4, pp. 5-6.](https://arxiv.org/pdf/2610.14224v1#page=5)

### Figure 5: both recursion forms improve in the plotted range

On WorkBuddy Code and Office with Gemini/OpenCode, both parallel and sequential curves rise monotonically over **k=1 through 5**. Parallel moves **76.5 to 80.8** on Code and **79.5 to 83.4** on Office. Sequential is higher on Code at k=2; parallel finishes higher at k=5. Both forms at k=2 exceed every plotted baseline at k=5 in these two domains. This is evidence for the examined budgets and tasks, not a promise of monotonic scaling indefinitely. Intermediate curve points have not been digitized into the guide's data. [Figure 5 and discussion, pp. 9-10.](https://arxiv.org/pdf/2610.14224v1#page=9)

### Figure 6: empirical compute/performance trade-off

The x-axis is **total compute per task in millions of tokens**, on a logarithmic scale, counting execution and improvement **before final submission**. It is not latency, dollar cost, or the executor's #Steps. The y-axis is gain over base.

For Gemini/OpenCode, increasing k from 1 to 5 moves the reported gain **4.5 to 7.5** on JobBench and **5.1 to 8.4** on WorkBuddy. Both Harness2 configurations are on the empirical frontier among the plotted methods; Meta-Harness uses more compute than Harness2 at k=5 for a lower score. This is a frontier for the compared measurements, not evidence of universal cost optimality. Exact token coordinates are not supplied as numeric data in the figure and have not been inferred here. [Figure 6, p. 10.](https://arxiv.org/pdf/2610.14224v1#page=10)

### Figure 7: two distinct tests of the improvement library

The left panel directly edits the base harness **without current-task reference executions or candidate probes**. Its k labels identify the budget used to build the supplied library, rather than fresh task-level probing. The right panel adds JobBench experience to **one-step WorkBuddy refinement**. These are different interventions.

| WorkBuddy domain | Base | Direct edit, no library | Direct edit, k=1 library | Direct edit, k=5 library | One-step refinement | One-step + JobBench experience |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Code | 73.4 | 63.2 | 73.8 | 74.3 | 76.5 | 77.1 |
| Web | 69.9 | 65.0 | 72.6 | 74.3 | 76.4 | 76.9 |
| Office | 74.0 | 77.1 | 77.5 | 79.1 | 79.5 | 82.4 |

The k=5 library supports direct-edit gains over base of **0.9, 4.4, and 5.1** points. JobBench transfer adds **0.6, 0.5, and 2.9** points to ordinary one-step refinement. The latter is evidence of cross-benchmark reuse in the tested direction, not unrestricted transfer across arbitrary domains. [Figure 7 and discussion, pp. 10-11.](https://arxiv.org/pdf/2610.14224v1#page=10)

## Ablations

**Table 3 isolates improvement mechanisms at k=1**, with Gemini/OpenCode. Removing scoping retains two generic editors and the same candidate/probe budget; removing composition still probes both candidates, then selects one. These controls make the interpretation more specific than “using fewer components lowers performance.”

| Configuration | WorkBuddy Avg. | Loss from full | JobBench | Loss from full |
| --- | ---: | ---: | ---: | ---: |
| Harness2 | 77.5 | - | 36.0 | - |
| Without library reads/writes | 74.4 | 3.1 | 34.2 | 1.8 |
| Without invariant/domain scoping | 74.6 | 2.9 | 32.3 | 3.7 |
| Without composition | 75.9 | 1.6 | 34.1 | 1.9 |

These comparisons support contributions from all three mechanisms in these settings. Table 3 provides point values without SDs. [Table 3 and ablation definitions, p. 10.](https://arxiv.org/pdf/2610.14224v1#page=10)

**Table 6 asks a different question:** after k=5 refinement, remove component groups from the finished harness and re-evaluate, without letting improvement compensate. Removing skills loses **5.3** macro-average points; removing scripts loses **3.7**; removing the prompt-related group loses **1.5**. Skills have the largest Code/Web effect, while scripts have the largest Office effect. These losses are not additive causal shares: the groups can interact. “Prompt*” is the paper's grouped prompt-related category, not a result for the system prompt alone. [Appendix E.1 and Table 6, p. 23.](https://arxiv.org/pdf/2610.14224v1#page=23)

## Supplementary evidence

| Evidence | What it shows | Boundary on the interpretation |
| --- | --- | --- |
| Figure 8, p. 11 | All five tested models improve on all three benchmarks when the same model edits and executes, with OpenCode at k=2 | A separate editor configuration from the main tables; “same-model” gains do not imply the default editor never matters |
| Figure 10, pp. 23-24 | Library provenance appears in 22% of modified files on LAB/Office and 47% on JobBench; only 2-10% retain at least half their lines | Provenance uses a line-containment heuristic excluding common boilerplate; it is not a causal estimate of library value |
| Figure 11, p. 24 | Completed-library leave-one-out re-runs reach 79.4 versus 77.5 on WorkBuddy and 37.7 versus 36.0 on JobBench | Each task's own entry is removed, but later tasks' entries are available; this is **offline reuse**, and repeated execution may contribute |
| Figure 12, p. 24 | A harness refined for Gemini 3.5 Flash benefits three other tested executors on Code/Office without further adaptation | Transfer magnitude varies by executor and domain |
| Table 7, p. 25 | Tool-error rates fall 0.8% to 0.5% on WorkBuddy, 14.4% to 9.1% on JobBench, and 2.0% to 1.6% on LAB, for Gemini/OpenCode at k=1 | Calls fall on WorkBuddy but increase on JobBench and LAB; reliability is different from minimizing calls |
| Figure 13, p. 25 | OpenCode-based Harness2 at k=5 exceeds the strongest unchanged production harness in each WorkBuddy domain | Additional test-time compute is part of the intervention |
| Figure 14, pp. 25-26 | Nine regressions expose weak selection, restrictive/shared assumptions, execution variability, and judging failures | Scores in this retrospective analysis are unavailable to the pipeline |
| Figures 9 and 15-19, pp. 12, 27-29 | Concrete edits connect observed execution failures to better re-runs across domains | Illustrative case studies; not controlled isolated attribution of each edit |

Sources: [Figure 8, p. 11](https://arxiv.org/pdf/2610.14224v1#page=11), [Appendix E, pp. 23-29](https://arxiv.org/pdf/2610.14224v1#page=23).

The strongest caution in the failure analysis is operational: a score-blind selector can reject a better candidate, and all candidates can share a bad premise. A model-generated checker can agree with the very assumption that made the edit wrong. Better-looking execution evidence therefore does not become a correctness verifier merely because it is repeated.

## Limits on the conclusions

Three streams and reported SDs characterize variation, but Tables 1-3 do not report confidence intervals, statistical significance tests, or an isolated causal estimate for every mechanism. The benchmark scores use different judges and rubrics, so their numeric levels should not be compared as a common measure of task difficulty.

The evaluation covers bounded k values and selected professional-task suites. It supports improvement under those configurations; it does not establish unbounded recursive self-improvement, guaranteed correctness, universal transfer, or a globally optimal cost allocation. The paper itself notes additional inference cost, shared model biases, execution variability, and the need for future library management and adaptive stopping. [Limitations and future directions, p. 29.](https://arxiv.org/pdf/2610.14224v1#page=29)

## Data notes

The [reported-results JSON](../data/reported-results.json) contains complete transcriptions of Tables 1-4 and supplementary Tables 6-7, selected exact chart labels, units, page locators, and a 12-row derived summary. It stores SDs separately from means and recursion deltas separately from both. Table 4's booleans represent the authors' taxonomy under Appendix A.1's definitions.

The JSON deliberately omits invented uncertainty estimates and precise coordinates guessed from curve plots. Derived totals use already rounded inputs and should not be mistaken for raw experimental outputs.

Two cross-analysis baseline discrepancies are preserved: **Figure 12 uses a GLM-5 Code base of 58.5, while Table 1 reports 58.4; its Office base is 73.7, while Table 1 reports 75.1**. The guide uses each source's value in its own context rather than silently rewriting either. The appendix result is a separate transfer analysis; v1 does not explain the differences. [Table 1, p. 8; Appendix E.3, p. 24.](https://arxiv.org/pdf/2610.14224v1#page=24)

[Previous: Method](02-method.md) · [Overview](../README.md) · [Next: Critical reading](04-critical-reading.md)

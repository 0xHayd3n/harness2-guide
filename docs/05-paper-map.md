# 5. Paper map

[Previous: critical reading](04-critical-reading.md) · [Overview](../README.md) · [Next: discussion](06-discussion-and-reproduction.md)

This map covers **arXiv:2610.14224v1**, *Harness2: Recursive Agent Harnessing for an Open World*, in its 37-page PDF. Page references below use the PDF's printed page numbers, which match the PDF page positions. Links open the pinned [v1 PDF](https://arxiv.org/pdf/2610.14224v1); a PDF viewer may ignore the page fragment. Descriptions are original reading aids, not reproductions of the paper's figures or prompts.

## Reading routes

- **Understand the mechanism:** §§2.1–2.3, pp. 3–7 → Figures 2–4 → Appendix D, pp. 20–22 → Prompts 1–6, pp. 30–37.
- **Assess the headline evidence:** §3, pp. 7–9 → Tables 1–2 → §4, pp. 9–12 → Appendices B–C, pp. 18–20.
- **Assess what the evidence does not establish:** Appendix E.1–E.6, pp. 23–26 → Appendix F, p. 29 → [critical reading](04-critical-reading.md).
- **Learn from concrete behavior:** Figure 9, p. 12 → Figures 14–19, pp. 26–29 → Appendix H's attribution instructions, pp. 36–37.

## Main text, section by section

| Section | Pages | What to look for |
|---|---|---|
| Title, authors, abstract, Figure 1 | [1](https://arxiv.org/pdf/2610.14224v1#page=1) | Two levels of recursion; summary gains; Figure 1's particular Gemini 3.5 Flash/OpenCode setting. |
| §1 Introduction | [1–3](https://arxiv.org/pdf/2610.14224v1#page=1) | Unseen deployment tasks, absent correctness labels, and the distinction between refining a task harness and improving future refinement. |
| §2 Harness2 | [3–7](https://arxiv.org/pdf/2610.14224v1#page=3) | Framework and notation; not an additional experimental section. |
| §2.1 Recursive Agent Harnessing | [3–4](https://arxiv.org/pdf/2610.14224v1#page=3) | Frozen model; eight editable components; every new task starts at the common execution harness; the improvement library persists. |
| §2.2 Task-Level Recursion | [4–6](https://arxiv.org/pdf/2610.14224v1#page=4) | Current-task adaptation while the improvement harness stays fixed. |
| §2.2.1 A Contrastive Improvement Step | [4–5](https://arxiv.org/pdf/2610.14224v1#page=4) | Equation 1; Propose, Probe, Compose; behavioral contrast is evidence rather than correctness verification. |
| §2.2.2 Parallel and Sequential Recursion | [5–6](https://arxiv.org/pdf/2610.14224v1#page=5) | Equations 2–3; width versus chained refinement; anonymized final selection at `k > 1`. |
| §2.3 Harnessing-Level Recursion | [6–7](https://arxiv.org/pdf/2610.14224v1#page=6) | Reflect on the complete improvement record; Equation 4; store adopted harnesses and supported experience; reuse through later improvement. |
| §3 Experiments | [7–9](https://arxiv.org/pdf/2610.14224v1#page=7) | Three benchmarks, four executor/harness configurations, one-step and parallel `k=5` results. |
| §3.1 Experiment Setup | [7](https://arxiv.org/pdf/2610.14224v1#page=7) | Benchmarks, baselines, frozen executors, default editor, empty initial libraries, three streams with shuffled task order. |
| §3.2 Main Results | [8–9](https://arxiv.org/pdf/2610.14224v1#page=8) | Tables 1–2; improvements over the starting harness; a baseline exception on LAB; initial-harness gaps do not always shrink. |
| §4 Analysis: Effect of Task-Level Recursion | [9–10](https://arxiv.org/pdf/2610.14224v1#page=9) | Figure 5; parallel and sequential budget curves on WB-code and WB-office. |
| §4 Analysis: Compute-Performance Trade-off | [10](https://arxiv.org/pdf/2610.14224v1#page=10) | Figure 6 counts execution and improvement tokens before submission; reported empirical frontier, not a universal efficiency guarantee. |
| §4 Analysis: Ablation Study | [10](https://arxiv.org/pdf/2610.14224v1#page=10) | Table 3 removes the library, scoped roles, or composition at `k=1`; distinguish this from Table 6's post-improvement removals. |
| §4 Analysis: Analysis of Harnessing-Level Recursion | [10–11](https://arxiv.org/pdf/2610.14224v1#page=10) | Figure 7; direct editing with libraries built at different budgets; JobBench-to-WorkBuddy transfer; explicit retrospective qualification for Figure 11. |
| §4 Analysis: Same Model as Executor and Editor | [11](https://arxiv.org/pdf/2610.14224v1#page=11) | Figure 8 uses five models in the same-model setting at `k=2`; this is separate from the default editor configuration. |
| §4 Analysis: Case Study | [11–12](https://arxiv.org/pdf/2610.14224v1#page=11) | Figure 9's JobBench producer task; reconciliation and reopening generated files. |
| §5 Related Work | [12–13](https://arxiv.org/pdf/2610.14224v1#page=12) | Recursive Self-Improvement and Harness Optimization and Evolution; Appendix A defines the comparison taxonomy. |
| §6 Conclusion | [13](https://arxiv.org/pdf/2610.14224v1#page=13) | Authors' synthesis of current-task refinement and reusable improvement experience. |
| References | [13–16](https://arxiv.org/pdf/2610.14224v1#page=13) | Bibliographic sources; the related-method classifications in Table 4 remain the authors' analysis. |

## Complete appendix map

| Appendix or subsection | Pages | Content and reading purpose |
|---|---|---|
| Appendix contents | [17](https://arxiv.org/pdf/2610.14224v1#page=17) | Printed appendix navigation. |
| **A. Comparison of Harness Improvement Methods** | [17–19](https://arxiv.org/pdf/2610.14224v1#page=17) | Context for Table 4's method comparison. |
| A.1 Comparison Criteria | [17–18](https://arxiv.org/pdf/2610.14224v1#page=17) | Defines all six columns: Object, Stage, Label, Streaming, Scaling, Improver Update. The table itself is on p. 19. |
| **B. Benchmarks** | [18–20](https://arxiv.org/pdf/2610.14224v1#page=18) | Dataset sizes and splits, containers, judges, evaluation-only labels, stream protocol, and the meaning of `#Steps`. |
| **C. Baselines** | [20](https://arxiv.org/pdf/2610.14224v1#page=20) | Best-of-`k`, ReasoningBank, Harness Scaling, and Meta-Harness adaptations, budgets, retrieval, and fallbacks. |
| **D. Implementation Details** | [20–22](https://arxiv.org/pdf/2610.14224v1#page=20) | Runtime, validation, library organization, editable surface. |
| D.1 Executors and Initial Harnesses | [21](https://arxiv.org/pdf/2610.14224v1#page=21) | Stock agent plus benchmark instructions; OpenCode files versus Codex `AGENTS.md`; placeholders; 200-turn/3,600-second rollout limits. |
| D.2 Improvement Sessions and Library Configuration | [21](https://arxiv.org/pdf/2610.14224v1#page=21) | Claude Opus 4.8 editor/selector at high effort; evidence supplied as files; score/rubric guard; one retry after invalid-tree validation; per-domain libraries. |
| D.3 Editable Harness Components | [22](https://arxiv.org/pdf/2610.14224v1#page=22) | Table 5's paths, activation times, and definitions for C1–C8. |
| **E. Supplementary Experiments and Analyses** | [23–29](https://arxiv.org/pdf/2610.14224v1#page=23) | Additional evidence, failure analysis, and successful examples. |
| E.1 Contributions of Harness Components | [23](https://arxiv.org/pdf/2610.14224v1#page=23) | Table 6 removes prompt-related parts, skills, or scripts from already improved harnesses, without rerunning improvement. |
| E.2 Reuse of Harnesses and Improvement Experience | [23–24](https://arxiv.org/pdf/2610.14224v1#page=23) | Figure 10's line-containment reuse measure; Figure 11's leave-one-out re-run with the completed library. |
| E.3 Transfer Across Executor Models | [24](https://arxiv.org/pdf/2610.14224v1#page=24) | Figure 12 deploys a Gemini 3.5 Flash-refined harness unchanged with GLM-5, Gemini 3.7 Flash, and Claude Opus 4.8 on Code and Office. |
| E.4 Tool-Use Reliability | [25](https://arxiv.org/pdf/2610.14224v1#page=25) | Table 7: tool-error rates fall, but tool-call counts do not uniformly fall. |
| E.5 Comparison with Production Harnesses | [25](https://arxiv.org/pdf/2610.14224v1#page=25) | Figure 13 compares fixed production harnesses to OpenCode plus Harness2 at `k=5`; additional refinement compute matters. |
| E.6 Failure Analysis | [25–26](https://arxiv.org/pdf/2610.14224v1#page=25) | Figure 14's nine regressions: selection, restrictive edits/shared assumptions, execution variability, evaluation failure, and ineffective targeting. |
| E.7 Qualitative Case Studies | [26–29](https://arxiv.org/pdf/2610.14224v1#page=26) | Figures 15–19: Code, Office, Web, LAB arbitration, and a JobBench task with all eight components edited. |
| **F. Limitations** | [29](https://arxiv.org/pdf/2610.14224v1#page=29) | Two explicit limitations: cost of recursive refinement and reliability of execution-based feedback. |
| **G. Future Directions** | [29](https://arxiv.org/pdf/2610.14224v1#page=29) | Library consolidation, outdated-experience revision, retrieval refinement, and adaptive recursion allocation/stopping. These are proposed directions. |
| **H. Prompts** | [30–37](https://arxiv.org/pdf/2610.14224v1#page=30) | Shared benchmark-independent improver prompts; benchmark-specific appended blocks are referred to the code release. |

### Prompt-by-prompt map

Appendix H does not print six wholly independent prompts: it prints shared material once and gives replacements or differences elsewhere. A reading that treats each printed block as a complete standalone executable prompt will miss shared instructions.

| Prompt | Pages | Role and important contract |
|---|---|---|
| 1. Harness Editor, invariant scope | [30–33](https://arxiv.org/pdf/2610.14224v1#page=30) | Diagnose process/tool/completion failures from concrete trajectory moments; choose a component; recheck copied workspace facts; treat evidence as data; validate the whole harness; preserve requested artifact shape; edit files and return evidence notes. |
| 2. Harness Editor, domain scope | [33](https://arxiv.org/pdf/2610.14224v1#page=33) | Replaces Prompt 1's dimension section. Encode practitioner operations, artifact contracts, and decision rules; require sources; keep task facts separate from durable domain memory. |
| 3. Harness Composer, parallel recursion | [33–34](https://arxiv.org/pdf/2610.14224v1#page=33) | Reads `k` base rollouts and `2k` probed proposals; merge, revise, adopt, or keep the base; consider downside and empty outputs; record each decision with evidence. Several sections are inherited from Prompt 1. |
| 4. Harness Composer, sequential | [34–35](https://arxiv.org/pdf/2610.14224v1#page=34) | Printed differences from Prompt 3. Use prior checkpoints and all earlier evidence; an earlier rejected edit can be restored. Here keeping the base means keeping the **current checkpoint**, not restoring the original harness. |
| 5. Terminal aggregator: blind selection | [35–36](https://arxiv.org/pdf/2610.14224v1#page=35) | Compares anonymized rendered artifacts against request/source; priorities are delivery, conformance, fidelity, consistency, operational fitness, finish. Returns one existing answer; does not synthesize a new one. |
| 6. Experience Reflector | [36–37](https://arxiv.org/pdf/2610.14224v1#page=36) | Diff every candidate, including rejected ones; classify observed edit effects; prefer confounded attribution when isolation is absent; retain at most one supported transferable lesson, or decline a lesson entry. |

## Every figure

| Figure | Page | Subject | Qualification to retain |
|---|---|---|---|
| **1** | [1](https://arxiv.org/pdf/2610.14224v1#page=1) | Overall WorkBuddy-Bench results and a WB-code scaling curve. | Left panel is Gemini 3.5 Flash/OpenCode with parallel `k=5`; it is not the complete evaluation matrix. |
| **2** | [3](https://arxiv.org/pdf/2610.14224v1#page=3) | Eight harness components grouped by runtime role. | Skills load on invocation, subagents add their own context, plugins operate in the tool loop; these are different mechanisms. |
| **3** | [5](https://arxiv.org/pdf/2610.14224v1#page=5) | Task-level and harnessing-level pipeline. | The improvement harness changes after a task; the current task's improvement harness stays fixed. |
| **4** | [6](https://arxiv.org/pdf/2610.14224v1#page=6) | Parallel versus sequential recursion. | In the implemented parallel scheme, `k` is population width for one update; sequential `k` is chained steps. |
| **5** | [9](https://arxiv.org/pdf/2610.14224v1#page=9) | Scaling budgets 1–5 on WB-code and WB-office. | Both Harness2 forms rise in these plotted settings; the figure does not establish unbounded monotonic scaling. |
| **6** | [10](https://arxiv.org/pdf/2610.14224v1#page=10) | Gain versus total token compute on JobBench and WorkBuddy-Bench. | Includes execution and improvement cost; empirical Pareto frontier is specific to the plotted methods/configurations. |
| **7** | [11](https://arxiv.org/pdf/2610.14224v1#page=11) | Direct editing with accumulated libraries; JobBench-to-WorkBuddy transfer. | Left removes reference/probe execution from the later editing test. Right is cross-benchmark library transfer, not cross-model transfer. |
| **8** | [11](https://arxiv.org/pdf/2610.14224v1#page=11) | Same model as executor and editor. | Five models under OpenCode at `k=2`; default main-table editor is separately Claude Opus 4.8. |
| **9** | [12](https://arxiv.org/pdf/2610.14224v1#page=12) | JobBench production-files case, 43.1 → 77.8. | Four retained component edits; illustrates a mechanism, not an isolated causal estimate per component. |
| **10** | [23](https://arxiv.org/pdf/2610.14224v1#page=23) | Library line containment and distribution of modified components. | Excludes common boilerplate lines; compares to the library available at refinement time; overlap is not proof of causal benefit. |
| **11** | [24](https://arxiv.org/pdf/2610.14224v1#page=24) | Leave-one-out reuse, WorkBuddy 77.5 → 79.4 and JobBench 36.0 → 37.7. | Completed library includes later tasks; this is retrospective reuse, and repeated execution may contribute. |
| **12** | [24](https://arxiv.org/pdf/2610.14224v1#page=24) | Unchanged cross-model deployment of an adopted harness. | Code and Office only; gains vary by executor/domain. The GLM-5 Code base is shown as 58.5 here, versus 58.4 in Table 1. |
| **13** | [25](https://arxiv.org/pdf/2610.14224v1#page=25) | CodeBuddy, OpenCode, Codex, Claude Code, and adapted OpenCode. | Fixed alternatives versus Harness2 with extra `k=5` refinement compute. |
| **14** | [26](https://arxiv.org/pdf/2610.14224v1#page=26) | Nine regressions in three categories. | Scores are retrospective evaluations, unavailable to the pipeline; see the [failure-case analysis](04-critical-reading.md#nine-regressions-worth-reading). |
| **15** | [27](https://arxiv.org/pdf/2610.14224v1#page=27) | Code router task, 60.0 → 100.0. | One tool-guidance edit addresses pseudo tool calls emitted as text. |
| **16** | [27](https://arxiv.org/pdf/2610.14224v1#page=27) | Office channel/quarter aggregation, 23.6 → 100.0. | Skill and guardrails establish grain, derived metrics, cleaning, and exact requested workbook shape. |
| **17** | [28](https://arxiv.org/pdf/2610.14224v1#page=28) | Offline CSV mapping wizard, 64.0 → 100.0. | Skill, script, guardrail address state transitions and offline operation, not appearance alone. |
| **18** | [28](https://arxiv.org/pdf/2610.14224v1#page=28) | LAB arbitration redline, 44.4 → 94.5. | In-body markup survives the case's text conversion; do not infer that native tracked changes are generally inappropriate. |
| **19** | [29](https://arxiv.org/pdf/2610.14224v1#page=29) | JobBench social-science research assistant, 72.0 → 100.0. | Claude Opus 5 serves as both roles; all eight components are written, while the figure highlights examples from that larger edit. |

## Every table

| Table | Page | What it contains | How to read it |
|---|---|---|---|
| **1** | [8](https://arxiv.org/pdf/2610.14224v1#page=8) | WorkBuddy-Bench Code/Web/Office, domain macro-average, execution steps; two models × two initial harnesses. | Parentheses are SD over runs; `+ Recursion` entries are changes after parallel `k=5`, not absolute results. Avg. SD is over per-run domain averages. |
| **2** | [9](https://arxiv.org/pdf/2610.14224v1#page=9) | JobBench Score and LAB Partial, plus steps, for the same model/harness matrix. | LAB is a per-criterion pass rate, not all-criteria task success. Bold results are best **before** recursion. |
| **3** | [10](https://arxiv.org/pdf/2610.14224v1#page=10) | Library, scoping, composition ablations at `k=1`. | Controlled removal of improvement mechanisms with Gemini 3.5 Flash/OpenCode; not the eight-component ablation. |
| **4** | [19](https://arxiv.org/pdf/2610.14224v1#page=19) | Comparison of harness-improvement methods on six axes. | Read Appendix A.1 first. A marked improver update records a mechanism, not verified gains in improving ability. |
| **5** | [22](https://arxiv.org/pdf/2610.14224v1#page=22) | C1–C8: files, activation, definitions, runtime groups. | OpenCode component surface; Codex places the always-on instructions in `AGENTS.md` per D.1. |
| **6** | [23](https://arxiv.org/pdf/2610.14224v1#page=23) | Post-improvement removal of prompt-related components, skills, or scripts at `k=5`. | No re-optimization to compensate for removed parts. Effects are not additive; the prompt group is grouped rather than a per-file ablation. |
| **7** | [25](https://arxiv.org/pdf/2610.14224v1#page=25) | Average tool-call counts and tool-error rates at `k=1`. | Error-rate reductions are distinct from call-count reductions; JobBench and LAB use more calls. |

## All numbered equations and notation

The following are compact restatements of the four numbered equations, with the paper's symbols retained where useful. They describe state flow, not a correctness proof.

| Equation | Page | Restatement | Meaning |
|---|---|---|---|
| **(1)** | [4](https://arxiv.org/pdf/2610.14224v1#page=4) | `(H′, e′, ξ) = Φ(q_t, H, E; R_t)` | One contrastive step returns an executed successor and a record of evidence/decisions. The model and environment stay matched; `R_t` stays fixed during the task. |
| **(2)** | [6](https://arxiv.org/pdf/2610.14224v1#page=6) | `H′_j = Compose_j(q_t, H, B, P; R_t)`, `j = 1,…,k` | Independent parallel compositions read the same base execution set `B` and probed candidate pool `P`; each successor is executed. |
| **(3)** | [6](https://arxiv.org/pdf/2610.14224v1#page=6) | `(H^(r), e^(r), ξ^(r)) = Φ(q_t, H^(r−1), E^(r−1); R_t)`, `r = 1,…,k` | Sequential steps carry a checkpoint and accumulated history forward, starting at `H^(0) = H_0`. |
| **(4)** | [7](https://arxiv.org/pdf/2610.14224v1#page=7) | `R_(t+1) = Update(R_t, H*_t, D_t)` | After returning the task deliverable, update the improvement library with the adopted harness and supported reflection from the full task record. |

Other notation introduced in §§2.1–2.3:

- `M`: frozen model; `H = (h_1,…,h_m)`: editable harness components, with `m=8` in this paper; `A(·; M, H)`: the agent formed from model plus harness.
- `q_t`: current task in the arriving stream; `H_0`: common execution starting point for each new task.
- `e = (τ, y)`: execution record, consisting of trajectory and deliverable. The initial reference is sampled from the agent under the current harness.
- `E`: task-local execution/improvement history; `ξ`: one step record; `D_t`: complete record used for reflection.
- `R_t`: improvement harness, evolving across tasks through its library. Stage instructions, model weights, and the decision rule remain fixed (§2.3, p. 7).
- `H*_t`: **adopted** harness. The star does not claim verified optimality (§2.2.2, p. 6).

## Source-sensitive details

Page 1 prints a document date of 2026-10-12, while the arXiv margin identifies v1 as 9 October 2026. Keep version identification anchored to **2610.14224v1**, rather than treating those printed dates as interchangeable. Figure 12's GLM-5 baselines are 58.5 on Code and 73.7 on Office, while Table 1's corresponding main-table bases are 58.4 and 75.1; the guide preserves each analysis's context instead of silently reconciling the values.

This map describes the pinned paper, including its appendix prompts. It does not claim the current authors' repository implements every printed detail, and it is not a reproduction or experimental run.

[Previous: critical reading](04-critical-reading.md) · [Overview](../README.md) · [Next: discussion](06-discussion-and-reproduction.md)

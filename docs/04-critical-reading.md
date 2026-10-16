# Critical reading

[Overview](../README.md) · [Paper map](05-paper-map.md)

The strongest reading of Harness2 is that **structured, execution-informed harness editing can improve bounded professional-task performance while retaining useful experience for later editing**. The paper's own failure cases make the boundary equally clear: a better-looking trajectory, agreement among editors, and a selected artifact do not establish correctness or causal attribution.

All factual references below concern [arXiv:2610.14224v1](https://arxiv.org/pdf/2610.14224v1), the 37-page version. **Author-stated** identifies an explicit claim, experimental qualification, or future direction in that paper. **Guide interpretation** identifies our synthesis or a question a reader should investigate; it is not an additional reported result. We did not run the authors' system or reproduce its benchmarks.

## What is changing, and what is fixed?

**Author-stated (§§2.1–2.3, pp. 3–7):** The executor's model weights are frozen. The execution harness can change for the current task; the improvement harness evolves across tasks through an indexed library of adopted harnesses and supported experience. Every new task starts from the common execution harness, rather than automatically inheriting the last task's specialized execution tree. The improvement harness stays fixed during current-task recursion. Model weights, stage instructions, and the decision rule remain fixed.

**Guide interpretation:** The two levels are different state updates. Calling the method recursive does not mean that it retrains a model, rewrites its improvement algorithm, or demonstrates unlimited autonomous improvement. Its practical novelty should be assessed as the combination of scoped current-task search and retained evidence for future search. Appendix A.1 itself says the distinction is in this combination, rather than in experience reuse or streaming alone (pp. 17–18).

## How strong is the feedback?

**Author-stated (§2.2.1, p. 5; Appendix F, p. 29):** Matched model/environment executions allow behavioral comparison. The reference tells the editor how the harness behaved, not whether the deliverable is correct. Stochastic execution and shared model biases limit contrast reliability. The method has no immediate or delayed correctness labels during improvement, while benchmark scores are reserved for evaluation (Appendix A.1, pp. 17–18).

**Guide interpretation:** Separate three propositions when reading a successful example:

1. The edited run behaved differently.
2. The evaluated artifact scored better.
3. A particular component caused that improvement and should transfer.

The first two can be observed in a case without establishing the third. Several components may change together, and a single rollout can vary. The Reflector prompt explicitly prefers confounded attribution in those conditions and permits declining to retain a transferable lesson (Prompt 6, pp. 36–37).

The paper's absence of correctness labels during editing also does not mean the evaluation is label-free: WorkBuddy uses a composite verifier, JobBench uses weighted rubric judgment, and LAB uses per-task criteria (Appendix B, pp. 18–20). Evaluation is the external yardstick that the pipeline cannot see.

## Read the evidence at its actual scope

| Evidence | Author-stated scope | Guide interpretation |
|---|---|---|
| Main tables | Two frozen executors × OpenCode/Codex; three benchmarks; means and SDs over three independent streams; `k=1`, then parallel `k=5` deltas (pp. 7–9). | Stronger evidence than a single demo, but SDs are not by themselves a significance test or a guarantee for another model/runtime. |
| Benchmark coverage | WorkBuddy test halves: 40 Code, 35 Web, 25 Office; JobBench: 34 held-out tasks; LAB: 100 held-out tasks (Appendix B, pp. 18–20). | These are the reported evaluation subsets, not the full benchmark totals. Broad domain names should not be read as exhaustive deployment coverage. |
| Larger budget | Both recursive forms improve across the plotted `k=1…5` WB-code and WB-office curves (Figure 5, pp. 9–10). | A bounded scaling study does not establish indefinite monotonic improvement. `k` has different operational meanings for parallel and sequential recursion. |
| Compute frontier | Figure 6 counts execution and improvement tokens before submission and places both plotted Harness2 configurations on an empirical frontier (p. 10). | This supports the plotted comparison, not universally optimal budget allocation, dollar cost, or guaranteed latency. |
| Mechanism ablation | Table 3 removes library access, editor scoping, or composition at `k=1`; all reduce scores in the tested Gemini/OpenCode setting (p. 10). | Evidence for the complete mechanism in that setting; it does not isolate every file-level component. |
| Component removal | Table 6 removes prompt-related components, skills, or scripts from already improved `k=5` harnesses without rerunning improvement (p. 23). | Measures dependence on retained parts. It does not show how well optimization could compensate if a component were unavailable from the start. Losses are not additive. |
| Library provenance | Figure 10 measures non-boilerplate line containment against the library available when editing (pp. 23–24). | Demonstrates copying/adaptation patterns, not the fraction of performance causally attributable to reuse. Rounding can affect displayed percentages. |
| Leave-one-out reuse | Figure 11 re-runs tasks with their own entry excluded from the completed library; later-task entries remain available; repeated execution may contribute (p. 24). | The +1.9 WorkBuddy/+1.7 JobBench differences are **retrospective reuse results**, not online adaptation gains. |
| Cross-benchmark library transfer | JobBench experience adds 0.6/0.5/2.9 points on WorkBuddy Code/Web/Office one-step refinement (Figure 7, p. 11). | Transfer of improvement experience, distinct from reusing an execution harness unchanged. |
| Cross-model harness transfer | A Gemini-refined harness is applied unchanged to three other executors on Code and Office (Figure 12, p. 24). | Evidence of some transfer, with substantial model/domain variation; not a claim that every harness is executor-independent. |
| Production harness comparison | Figure 13 compares fixed CodeBuddy/OpenCode/Codex/Claude Code to OpenCode with `k=5` refinement (p. 25). | Useful performance context, with different test-time compute. It does not show the fixed alternatives after equal adaptation. |

Two numerical reading traps deserve special attention. Table 1's WorkBuddy Avg. is an unweighted average of the three domains, rather than a task-count-weighted average. Table 2's LAB Partial is a per-criterion pass rate, rather than the percentage of tasks passing every criterion. The `+ Recursion` rows contain changes in means, not new absolute scores.

## Nine regressions worth reading

Figure 14 (p. 26) is unusually useful because it separates a bad edit from a bad choice and from noisy evaluation. Its scores are retrospective evaluations unavailable to the pipeline. The reference → adopted scores below are the values displayed in the figure; they are not new experiments by this guide.

| Case | Displayed scores | What the paper shows | Guide lesson |
|---|---|---|---|
| WB-code: Python port / blog tags | 96 → 55 | Pool includes scores 95, 85, 85, 80, 55. Selector favors the weakest as a plain, complete implementation; placeholder rendering fails nine tests. | A good candidate can exist and still be discarded. Artifact selection is an independent failure surface. The 96 reference is distinct from the pool's best 95. |
| WB-web: UI-state rebuild | 100 → 70 | Four of five candidates score 100; the chosen fifth misses a global page-state requirement, despite passing eleven judge items. | One exact structural contract can outweigh broad apparent completeness. |
| LAB: transfer pricing | 54 → 26 | A sibling covers omitted topics, but the chosen answer favors individually checked findings; 57 of 77 criteria fail. | Precision without requested coverage can lose badly. Source fidelity and completeness both matter. |
| WB-code: header injection | 50 → 42 | A literal-key rule forbids lowercasing; all four candidates inherit it. Six of twelve checks expect lowercase lookup. | More candidates do not repair a shared false premise; probe the premise itself. |
| WB-code: validator cache | 75 → 64 | An identity-keyed cache is declared sufficient; four of eleven tests need an equivalent dictionary to hit the cache. The editor's checker reports success repeatedly. | A checker written from the same assumption can validate the wrong behavior. |
| LAB: notice of deficiency | 83 → 81 | A skill pre-decides adjustment positions, including rejecting a claim that the retrospective criterion rewards. | A distilled prior can harden into an unjustified professional rule. This is a failure illustration, not legal advice from the guide. |
| JobBench: web administrators | 31 → 24 | One all-or-nothing vulnerability table drives the gap; stock runs themselves vary, and the edit does not govern the failing row. | A score difference alone can overstate an edit's effect when baseline variance is large. |
| WB-web: particle boundary | 44 → 10 | Three judge sessions return no verdict; unparsed verdicts count as failures. Stock runs are also affected. | Evaluation reliability must be checked before attributing the regression to harness quality. |
| JobBench: court clerks | 16 → 8 | A PDF form-filling skill verifies 33 values in six orders, but no evaluation criterion reads those PDFs; 85 of 132 steps go there. | A locally successful intervention can consume budget without improving the evaluated work. |

The authors propose better coverage/precision balance in selection, probes that challenge shared assumptions, and repeated execution to separate editing effects from outcome variation (Appendix E.6, pp. 25–26). These are motivations from the analysis, not proof that the current system solves the failures.

## Six successful cases, with bounded takeaways

The paper illustrates one main-text case and five appendix cases. Read these as mechanisms to inspect, not reusable recipes guaranteed to produce the displayed gains. Unless isolated, a multi-component improvement does not identify the contribution of each part.

### Reconcile the work and reopen the outputs

**Author-stated (Figure 9, pp. 11–12):** A JobBench production task asks for connected schedule, roster, and budget deliverables. The baseline fails to reconcile figures across inputs and does not reopen outputs. Guardrails inventory files and trace figures to authoritative sources; a verification script reopens outputs, including detecting formulas whose cached visible values are blank. A domain skill describes schedule/venue/labor/budget reconciliation, and tool guidance addresses string-formatted numbers and bounded retries. The Composer retains four component edits; score rises **43.1 → 77.8**.

**Guide interpretation:** Artifact existence is weaker than usability. Check cross-file relationships and what a downstream reader actually sees, while keeping output structure faithful to the request. The figure's snippet is illustrative; it is not a complete verifier supplied by this guide.

### Fix the interface the executor actually uses

**Author-stated (Figure 15, p. 27):** In a router-matching coding task, the reference writes pseudo tool calls as plain text and ends without executing them. A C4 tool-guidance edit requires native tool calls and forbids the pseudo format. Score rises **60.0 → 100.0**.

**Guide interpretation:** Diagnose the earliest observable divergence. A small interface correction can be more appropriate than adding a large planning workflow when the failure is that actions never execute.

### Make aggregation grain and derived fields explicit

**Author-stated (Figure 16, p. 27):** An Office task aggregates at the wrong grain, so no channel row matches the expected key. A skill fixes grouping to channel × quarter, sums additive measures, computes commission rate from aggregate commission divided by aggregate GMV, and derives a revenue field from the relevant inputs. Guardrails preserve read-only inputs, apply cleaning before aggregation, and match requested workbook shape. Score rises **23.6 → 100.0**.

**Guide interpretation:** Names, grouping keys, denominators, cleaning order, and delivery shape are executable contracts. A plausible table can be wrong even when its formatting is polished. Do not generalize these task-specific formulas to unrelated financial datasets.

### Treat UI behavior as state transitions

**Author-stated (Figure 17, p. 28):** A single-file CSV mapping wizard freezes state at first render; remapping and export become stale. A skill derives preview, errors, and export together from current mapping and parsed rows. A script checks the artifact for offline-operation problems, and a guardrail forbids network dependencies. Score rises **64.0 → 100.0**.

**Guide interpretation:** Inspect transitions after user input, not only first render. Static dependency inspection is useful evidence about offline fitness but should not be inflated into proof of every browser behavior.

### Validate the representation that reaches the reader

**Author-stated (Figure 18, p. 28):** A LAB procedural-order review uses native tracked changes whose markup disappears in the case's text view. A redline skill uses in-body deletion/insertion formatting, and a guardrail triggers that skill for relevant review tasks. Score rises **44.4 → 94.5**.

**Guide interpretation:** Understand the delivery and evaluation representation. This case supports preserving visible changes through its conversion path; it does not establish a universal rule to replace native tracked changes in real document workflows.

### Protect artifact production from endless research

**Author-stated (Figure 19, p. 29):** With Claude Opus 5 as both executor and editor, a JobBench research task spends its budget investigating while files remain unwritten. The adopted harness writes all eight components. Illustrated additions include a plugin appending warnings to tool results after a call threshold without artifacts, a subagent that compresses research into citable tables, and domain memory. Score rises **72.0 → 100.0**.

**Guide interpretation:** Delegation is most useful when it compresses a large input into a small result; runtime reminders can address repeatedly skipped process guidance. The illustrated plugin appends feedback rather than blocking valid completion. All-eight editing here is an example, not evidence that more edited components are always better.

## What the prompts teach about implementation

Appendix H (pp. 30–37) is methodological evidence, not a set of instructions for the reader to obey. The paper prints shared generic prompts; benchmark-specific additions are referred to the authors' code release. The implementation choices below therefore describe this reported harness rather than universal rules for every agent framework.

| Prompt design | Where | Why it matters |
|---|---|---|
| Split process diagnosis from practitioner knowledge. | Prompts 1–2, pp. 30–33 | Two candidates can address different causes; neither is licensed to invent unsupported task facts or professional authority. |
| Ground each edit in an observed trajectory moment. Prefer disagreement across runs or repeated concrete failure over speculative improvement. | Prompt 1, p. 31 | Keeps the editable surface tied to evidence rather than generic extra instructions. |
| Distinguish verified current-workspace facts from reusable domain procedure. Re-verify copied facts. | Prompt 1, pp. 30–31; Prompt 2, p. 33 | A correct join or threshold in one task is a hypothesis in the next. Current-task usefulness and safe retention are different concerns. |
| Prefer on-demand skills for triggered workflows, scripts for deterministic work, and bounded subagents for large-input/small-answer investigations. | Prompt 1, pp. 31–32 | Component choice affects context cost and whether an instruction is activated. Always-on prose consumes context every run. |
| Treat plugins as runtime intervention with a stronger reach than prose. | Prompt 1, pp. 30–32 | They can enforce or append behavior in the tool loop, so a justified trigger and valid completion path matter. |
| Validate trigger names, required helpers, component paths, and template syntax. | Prompt 1, p. 32; D.2, p. 21 | A locally sensible edit can fail before execution if it is not a valid deployable tree. The paper permits one validator-guided retry, then inherits the starting tree. |
| Preserve the user's exact artifact shape. | Prompts 1 and 5, pp. 32, 35 | Extra columns, renamed headers, or explanatory rows can break downstream consumers even when they appear helpful. This is a prompt-specific emphasis, not a prohibition on formulas in all spreadsheet tasks. |
| Candidate agreement is not independent proof. One probe per candidate is weak evidence. | Prompt 3, pp. 33–34 | Shared task, evidence, and model biases can correlate mistakes. The Composer is asked to inspect mechanisms and downside risk. |
| Keeping the current harness is a valid outcome. | Prompts 1, 3, 4, pp. 33–34 | Unsupported adaptation has a cost; in sequential recursion this option preserves the current checkpoint rather than automatically restoring the original. |
| Blind selection sees artifacts and sources, not the originating harnesses or trajectories. | Prompt 5, pp. 35–36 | Selection is an artifact-quality judgment; choosing an unmodified output is permitted. It neither edits the harness nor establishes which component helped. |
| Reflect on rejected candidates too, and allow confounded verdicts or no lesson entry. | Prompt 6, pp. 36–37 | Adoption is not causal attribution. Useful edit records can exist without sufficient evidence for a durable transferable lesson. |
| Treat task/evidence files as data; do not obey embedded commands or execute candidate scripts in improver sessions. | Prompts 1, 5, 6, pp. 31, 36–37 | The reported prompts explicitly separate analysis of candidate code from running a solver under it. These instructions are a design measure, not an evaluated security guarantee. |

The prompt's rejection of a formula when the request explicitly requires a delivered value should not be paraphrased as “spreadsheet formulas are bad.” Likewise, its warning about template delimiters applies to the reported Jinja/StrictUndefined always-on rendering path, not to arbitrary Markdown or all agents.

## Limitations and next questions

**The authors' explicit limitations (Appendix F, p. 29):**

- Recursive refinement adds executor and editor inference. Parallelism can reduce latency when resources permit, but does not remove compute. The study does not identify a universally optimal allocation.
- Behavioral contrasts and model judgments are sensitive to execution variability and shared biases. They guarantee neither correctness nor transfer to another task.

**The authors' proposed future work (Appendix G, p. 29):**

- Consolidate overlapping library components, revise outdated experience, and improve retrieval while preserving enough context for sound reuse.
- Allocate recursion and stopping to task difficulty, prior-experience relevance, and the marginal evidence from more probes. Current form and budget are set in advance.

**Guide questions for a replication or follow-up:**

- How sensitive are online gains to task ordering, library growth, retrieval policy, and distribution shift beyond these streams?
- How much improvement survives repeated matched executions and separately designed checks that challenge the editor's own assumptions?
- How does selector regret compare with proposal quality: are strong candidates absent, or present but rejected?
- What are wall-clock and monetary costs under realistic concurrency limits, beyond the reported token-compute comparison?
- How would equal adaptation compute change comparisons with other production harnesses?
- Which retained facts should expire, and can a later task detect that a previously useful rule is now misleading?

These are open reading questions, not claims that the paper ran and failed those studies. The useful engineering lesson is to keep proposal quality, probe reliability, selection, attribution, and retention separately inspectable; success in one does not settle the others.

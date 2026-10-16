# 2. Method: two feedback loops

[Overview](../README.md) · [Previous: concepts](01-concepts.md) · [Next: results](03-results.md)

## A task begins at H0

The task arrives with a common base execution harness H0 and a current improvement harness R_t. The latter contains the library available from earlier tasks in the domain. The execution harness can change during this task; R_t remains fixed until the task finishes. Models and environment configuration are held matched for candidate comparisons. [§2.1–2.2, pp. 4–5](https://arxiv.org/pdf/2610.14224v1#page=4).

The paper writes a contrastive improvement operation in Equation 1 as a map from the task, current harness, history, and improvement harness to a successor harness, its execution, and a step record. The record is essential: later reflection needs the candidates, probe outcomes, composition choices, and concrete evidence, not merely the final answer.

## Propose, Probe, Compose

| Stage | Reads | Produces | What the evidence can establish |
| --- | --- | --- | --- |
| Reference | Task and current execution harness | Trajectory and deliverable | How this harness behaved on a sampled run |
| Propose | Task, current tree, references, earlier local history, relevant library entries | An invariant candidate and a domain candidate | A grounded hypothesis about a repair, encoded as editable files |
| Probe | Each candidate with the same task/model/environment configuration | Candidate execution records | Whether the hypothesized behavior appears to change, and what regressions appear |
| Compose | Reference records, candidates, diffs, probe records, local history | A successor tree, explicit decisions, then an executed successor | A selective, auditable choice of edits; not external correctness |

Composition may merge complementary changes, revise conflicts, adopt a candidate wholesale, or keep the current harness. It is not forced concatenation. Each retained edit should connect to a specific observed behavior. The successor is executed, so the result is an actual output rather than an untested patch. [§2.2.1, pp. 4–5](https://arxiv.org/pdf/2610.14224v1#page=4).

The prompt implementation adds practical discipline: diagnose the earliest visible divergence, distinguish tool timeout from invalid input, avoid blind retries, preserve the requested artifact shape, make skills discoverable, and include their helpers. Candidate validation retries an invalid tree once; a second failure inherits the starting tree and records the fallback. [Appendix D.2, p. 21](https://arxiv.org/pdf/2610.14224v1#page=21), [Prompt 1, pp. 30–33](https://arxiv.org/pdf/2610.14224v1#page=30).

## Two ways to spend k

| | Parallel recursion | Sequential recursion |
| --- | --- | --- |
| Shared start | k base/reference executions | Initial history contains k base executions |
| Proposals | k invariant plus k domain candidates, independently proposed and probed | One invariant and one domain candidate per chained step |
| Composition | k independent sessions, each receiving the full reference and probe pool | Each step composes from its current harness and accumulated evidence |
| Recurrence | Generated harnesses/evidence inform successor compositions in one population update | The composed checkpoint becomes the starting point of the next step |
| Meaning of k | Exploration width | Refinement depth |

At k = 1, both reduce to the basic contrastive step. Parallel k = 5 is **not** five serial generations. Sequential history can support retaining, revising, or restoring earlier changes, including reconsidering an earlier rejected candidate. In its prompt, keeping the base means keeping the **current checkpoint**, not restoring H0. [Equations 2–3 and Figure 4, p. 6](https://arxiv.org/pdf/2610.14224v1#page=6), [Prompt 4, pp. 34–35](https://arxiv.org/pdf/2610.14224v1#page=34).

As a guide-derived execution count, the described parallel structure has k references + 2k probes + k composed-successor executions, or 4k executor rollouts before final selection. That arithmetic excludes editor/composer/selector/reflector sessions, retries, and runtime contingencies; it is not a published token-cost formula. It explains why one improvement step is more work than one executor run.

## Final selection chooses; it does not synthesize

For k > 1, the agentic selector sees anonymized existing deliverables and the task/source material. It does not see the originating harness or execution trajectory, cannot use grading scores, and returns one existing output without synthesizing a new answer. Base outputs are eligible. At k = 1 selection is bypassed. [§2.2.2, p. 6](https://arxiv.org/pdf/2610.14224v1#page=6), [Prompt 5, pp. 35–36](https://arxiv.org/pdf/2610.14224v1#page=35).

The selector prompt prioritizes delivery, conformance to the requested artifact, fidelity to sources, internal consistency, operational fitness, and finish. These priorities are an assessment procedure, not a correctness oracle. Figure 14 supplies counterexamples where a poorer output is selected despite a better one being available.

## Reflection updates the improvement library

After returning the deliverable, reflection reads the **whole improvement record**, including rejected candidates. The selected answer is only one observation: it does not identify which component caused a gain or whether that component transfers. The adopted tree and supported reusable experience can then enter the library, summarized by Equation 4. [§2.3, pp. 6–7](https://arxiv.org/pdf/2610.14224v1#page=6).

Prompt 6 asks for edit-level attribution with outcomes such as helped, hurt, no observed effect, or confounded. A multi-component change or a single rollout can leave attribution confounded. It asks for at most one durable lesson with an applicability cue and evidence. Where no reusable contrast exists, no new experience lesson should be manufactured. [pp. 36–37](https://arxiv.org/pdf/2610.14224v1#page=36).

Libraries are indexed and organized by benchmark domain. They retain executable trees plus `EXPERIENCE.md`; later sessions inspect entries as needed. Reused files must be copied into the new harness, and old workspace facts must be checked again. The next task resets the execution tree to H0 but reads the updated library R_(t+1). Model weights, the stage instructions, and the improvement algorithm stay fixed. [Appendix D.2, p. 21](https://arxiv.org/pdf/2610.14224v1#page=21), [Prompt 1, p. 31](https://arxiv.org/pdf/2610.14224v1#page=31).

## Read the prompt appendix as part of the method

The six prompt roles cover editor scopes, parallel composition, sequential differences, blind selection, and reflection. They explain what otherwise sounds abstract:

- Always-on prose consumes context on every invocation. The editor is encouraged to encode triggered procedures as skills and deterministic operations as scripts.
- Existing candidate code is evidence to inspect, not instructions for an improver to obey or execute directly.
- A proposed deliverable must keep the fields, sheets, paths, and structure the user requested; extra explanatory material can break the artifact's contract.
- A single good candidate run is weak evidence. The composer should inspect mechanisms, weigh non-delivery risk, and retain a no-change option.
- A reflection should record uncertainty instead of laundering adoption into a causal lesson.

These are paper-described design choices, not measurements that they always succeed. Appendix H prints shared prompts and differences, with benchmark-specific blocks left to the code release. [pp. 30–37](https://arxiv.org/pdf/2610.14224v1#page=30).

[Previous: concepts](01-concepts.md) · [Next: results](03-results.md)

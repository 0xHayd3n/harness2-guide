# 1. Concepts: what improves, and what persists?

[Overview](../README.md) · [Next: method](02-method.md)

## The two objects

A **harness** is the runtime around a model: the instructions it receives, tools it can use, procedures it can load, workers it can delegate to, and code interposed in its tool loop. Changing that runtime can change agent behavior while leaving the model parameters frozen.

The **execution harness** governs work on a task. The **improvement harness** governs how the system proposes and assesses changes to that execution harness. Harness² couples their updates, rather than treating the editor as a permanently fixed source of task-specific rewrites. In this implementation, the improvement harness changes through a library, not through rewritten stage prompts or trained editor weights. [§2.1–2.3, pp. 3–7](https://arxiv.org/pdf/2610.14224v1#page=3).

| State | Changes within one task? | Changes across tasks? |
| --- | --- | --- |
| Executor/editor model weights | No | No |
| Task's execution harness | Yes, through proposed and composed file edits | Next task resets to common H0; previous trees can be selectively reused through the library |
| Improvement library | Fixed while that task is refined | Retains adopted trees and evidence-supported improvement experience |
| Stage instructions and decision rule | Fixed | Fixed |
| Task-local execution history | Accumulates references, probes, decisions, and successors | Supplies reflection; completed tasks are not replayed in the online protocol |

The distinction matters. Carrying forward an entire task-specialized harness could import the wrong facts or procedure. A library makes prior components available for selective adaptation, with explanations of when they worked. Reuse still requires checking facts against the new task. [§2.3, p. 7](https://arxiv.org/pdf/2610.14224v1#page=7).

## Eight editable components

These are the paper's component IDs, not a ranking. Paths describe the OpenCode decomposition; Codex stores the always-on text in `AGENTS.md`. [Figure 2, p. 3](https://arxiv.org/pdf/2610.14224v1#page=3), [Appendix D, pp. 21–22](https://arxiv.org/pdf/2610.14224v1#page=21).

| ID | Component and representative path | Runtime role | Example of an appropriate change |
| --- | --- | --- | --- |
| C1 | System prompt, `systemprompt.md` | Every-call role and top-level procedure | A short standing completion procedure |
| C2 | Guardrails, `guardrails.md` | Every-call constraints | Preserve requested artifact structure |
| C3 | Memory, `LongTermMEMORY.md` | Every-call durable domain facts | A verified fact applicable across that domain |
| C4 | Tool guidance, `tool_descriptions/tool_guidance.md` | Every-call guidance for existing tools | Use actual tool calls rather than writing pseudo-calls as prose |
| C5 | Subagents, `sub_agents/<name>/AGENT.md` | Delegated worker in its own context | Read a large source set and return a small evidence table |
| C6 | Skills, `skills/<name>/SKILL.md` | Procedure loaded when invoked | A triggered cross-file reconciliation workflow |
| C7 | Scripts, `scripts/<name>.py` | Deterministic capability executed through the shell | Reopen a workbook and check its written output |
| C8 | Plugin, `plugin/<name>.ts` | Code acting around tool calls/turn boundaries | Append a bounded reminder when repeated research leaves artifacts unwritten |

The guide examples paraphrase cases and prompts, not reusable production rules. A plugin's enforcement power is a property of that runtime hook, not proof its policy is correct. A skill must be discoverable, and a helper it names must actually be shipped. A subagent adds a context, which helps only when the delegated boundary is useful. [Table 5, p. 22](https://arxiv.org/pdf/2610.14224v1#page=22), [Prompt 1, pp. 30–32](https://arxiv.org/pdf/2610.14224v1#page=30).

## Open world has a specific meaning here

The setting is a stream of tasks unavailable during harness design. During improvement there is no ground-truth answer, rubric, or task score. Repeated execution of the **current** task is allowed within a budget. The online procedure cannot revisit completed tasks or see future requests. Benchmarks still have external evaluation protocols, used afterward to measure submitted outputs. [§2.1, p. 4](https://arxiv.org/pdf/2610.14224v1#page=4), [Appendix A, pp. 17–18](https://arxiv.org/pdf/2610.14224v1#page=17).

Thus, label-free improvement does not mean there is no evaluation, and task-stream processing does not mean one execution per task. The authors' comparison table also distinguishes offline preparation from online adaptation: a method can have a label-free deployment phase after label-guided preparation.

## What counts as evidence?

An execution record includes a trajectory and a deliverable. A trajectory shows what the agent read, called, omitted, or failed to finish. A deliverable shows what it produced. A contrast between executions can connect a file edit to an observable behavior, but it can also reflect stochastic variation or a shared mistaken premise.

For example, the paper's Code case diagnoses a model emitting tool-call-looking text that never executes. Changing tool guidance has a visible mechanism: subsequent actions become actual calls. Its reported task score rises from 60 to 100, but that retrospective number was unavailable to the pipeline. [Figure 15, p. 27](https://arxiv.org/pdf/2610.14224v1#page=27).

By contrast, a checker authored from the same mistaken assumption as the edit can repeatedly report success while hidden tests still fail. That appears in the cache example in [Figure 14, p. 26](https://arxiv.org/pdf/2610.14224v1#page=26). Contrastive evidence should support a bounded behavioral conclusion, not a general correctness claim.

## Vocabulary to keep precise

| Term | Meaning in this guide |
| --- | --- |
| Invariant/general editor | Proposes workflow, tool-use, context, and completion changes that may recur across domains; it is not a formal mathematical invariant |
| Domain editor | Proposes practitioner knowledge, consistency checks, and domain-specific procedures |
| Compose | Selectively combine, revise, adopt, or retain executable harness components using evidence |
| Adopted harness | The harness associated with the chosen output; the star in the notation does not certify optimality |
| Reflection | Assess all edits and executions, including rejected candidates, before writing a transferable lesson |
| Recursion budget k | Width of one parallel population update, or number of sequential refinement steps |
| Partial | LAB's per-criterion pass rate; not the percentage of tasks passing every criterion |

[Previous: overview](../README.md) · [Next: method](02-method.md)

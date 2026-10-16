# 6. Discussion and reproduction planning

[Overview](../README.md) · [Previous: paper map](05-paper-map.md)

## Questions for a reading group

1. What observation would distinguish a harness improvement from a lucky execution? Compare the reference-set reasoning in Prompt 3 with the single-rollout ambiguity in Prompt 6. [pp. 33–37](https://arxiv.org/pdf/2610.14224v1#page=33).
2. Why reset the execution harness for each task while retaining the improvement library? What distribution shifts could still make a retrieved lesson harmful? [§2.3, p. 7](https://arxiv.org/pdf/2610.14224v1#page=7).
3. Which gains come from more candidate executions, which from scoped proposals, and which from composition? What additional compute-matched ablation would isolate them? [Figures 5–6 and Table 3, pp. 9–10](https://arxiv.org/pdf/2610.14224v1#page=9).
4. A blind selector can choose a weak output. Should selection optimize coverage, precision, conformance, or something task-dependent? What can be learned without seeing a hidden rubric? [Figure 14, p. 26](https://arxiv.org/pdf/2610.14224v1#page=26).
5. A larger library helps direct editing, but completed-library leave-one-out reruns see later experience. Which study supports online transfer, and which supports retrospective reuse? [Figure 7, p. 11](https://arxiv.org/pdf/2610.14224v1#page=11), [Figure 11, p. 24](https://arxiv.org/pdf/2610.14224v1#page=24).
6. Is an editor-authored checker evidence against the editor's own premise? How would you design a probe that challenges rather than repeats that premise? [cache failure, p. 26](https://arxiv.org/pdf/2610.14224v1#page=26).

## A protocol to specify before running

This repository has not executed the authors' system. The following is a guide-authored planning checklist for an independent study, not a claim that the public release reproduces the paper's exact setup.

| Decision | Record explicitly |
| --- | --- |
| Source | Paper version/hash; implementation commit; dependency/data revisions and licenses |
| Population | Exact task IDs, split, domain grouping, exclusions, and stream order for each replicate |
| Models | Executor, editor, selector, reflector, judge, exact model identifiers, reasoning settings, and routing |
| Initial state | H0 contents including benchmark instructions; empty library/memory; domain isolation |
| Budget | Parallel/sequential mode, k, model-turn and wall-clock caps, retry/fallback rules |
| Evidence isolation | Precisely what executor, improver, selector, and reflector can read, including network reachability |
| Evaluation | Judge model, metric denominator, failure/unparsed-verdict handling, score availability timing |
| Accounting | All executor and improvement tokens, cost assumptions, latency/concurrency, and offline search amortization |
| Uncertainty | Independent streams, task-order seeds, standard deviations, and handling of missing runs |
| Retention | Full trajectories, tree diffs, proposed/composed trees, selected output mapping, and lesson provenance |

The paper's experimental caps are 200 executor model turns and 3,600 seconds, with WorkBuddy's container timeout set to twice its benchmark default. Its baseline protocols include offline Meta-Harness search on separate training/development tasks; the other online methods begin with empty memory/library. These details are necessary to interpret comparisons. [Appendices B–D, pp. 18–22](https://arxiv.org/pdf/2610.14224v1#page=18).

## Current release is a separate source

The authors provide installation, deterministic demo, benchmark, and experiment instructions in their [repository](https://github.com/google-research/harness2). Consult those maintained instructions for supported environments rather than copying commands from this reading companion. The guide verified release commit `1cfe254e8d25b15f37048c3730134686abe60335` on October 16, 2026.

That release documentation describes unrestricted executor network access and a disabled Codex sandbox, reports a release-validation JobBench rollout obtaining its public rubric, uses locally generated partitions, gives a full LAB task count of 1,143, and leaves failed evaluations unscored. The pinned paper describes different population and evaluation details, including 1,251 LAB tasks overall and 100 evaluated, and a failure case where unparsed verdicts count as failures. These differences prevent treating a default current command as an exact reproduction. They do **not** establish rubric leakage in the paper experiments. [Pinned release experiment notes](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/EXPERIMENTS.md), [paper/release comparison](../SOURCES.md#paper-and-release-differences).

No benchmark commands or external candidate scripts were run while making this guide. A future study should resolve evidence access, split identity, and failure scoring before launching model-backed evaluation; those choices determine what the results measure.

## Useful follow-up studies

These are guide interpretations and research proposals, not reported experiments:

- Repeated, paired executions to estimate how much an apparent repair survives stochasticity.
- Compute-matched comparisons of generic editors, scoped editors, candidate-only selection, and composition across more task distributions.
- Selection diagnostics separating candidate quality from the ability to choose it without hidden scores.
- Controlled contamination tests with explicit network policy and logs, without extrapolating release-validation behavior to the paper.
- Library aging and contradictory-lesson studies that keep online and retrospective protocols separate.
- Adaptive stopping that measures both current-task returns and the value of experience to future tasks.

The last two directions overlap with the authors' proposed library management and adaptive recursion in [Appendix G, p. 29](https://arxiv.org/pdf/2610.14224v1#page=29). The paper does not establish these as implemented benefits.

[Previous: paper map](05-paper-map.md) · [Overview](../README.md)

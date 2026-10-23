# Automation skill adaptation

Status: Reviewable draft. Installed skills are unchanged. Base: `40e9d38238e487744ec216f5a57617e3c09cfb3e`.

| Responsibility | Owner |
| --- | --- |
| Automation lifecycle, layout, docs, logs, recovery, implementation branch | launchd-automation |
| Read-only investigation, plans, handoff, review | improve |
| Diagram generation and validation | archify |
| Skill draft, evaluation, feedback, refinement | skill-creator |

`candidate/` contains proposed skill packages. `baseline/` preserves the installed packages for comparison. Improve's candidate keeps its existing references. Launchd's candidate is instruction-only; existing scaffold, verifier, and templates need a separate compatibility update before installation.

## Evaluation and installation gate

Use `evals.json` for paired baseline and candidate runs in isolated fixtures. Use the same prompt, repository fixture, and permissions for each pair. Record outputs, checks, runtime, and any unauthorized mutation. Review the output with the user and refine the candidate through skill-creator. Then align launchd helpers and templates with the accepted contract, validate their behavior, and install the accepted packages.

Text and link checks are structural checks. They do not establish behavior or triggering quality. Paired behavior runs have not been performed. No installed skill, service, credential, or Notion record was changed.

See [plan 008](../008-opencode-model-refresh.md) and its [workflow](../008-automation-visual/automation.html).

Request 008 is now an intent and acceptance brief. Tool-owned automation source stays inside its tool repository; Space orchestration stays in Admin. Both report to explicit ignored runtime roots. The generic Improve candidate is superseded as a design direction by plan 010 and must be rewritten before installation. Full Superpowers design and implementation planning follow the request brief.

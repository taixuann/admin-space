<!-- CODEGRAPH_START -->
## CodeGraph

In repositories indexed by CodeGraph (a `.codegraph/` directory exists at the repo root), reach for it BEFORE grep/find or reading files when you need to understand or locate code:

- **MCP tool** (when available): `codegraph_explore` answers most code questions in one call — the relevant symbols' verbatim source plus the call paths between them, including dynamic-dispatch hops grep can't follow. Name a file or symbol in the query to read its current line-numbered source. If it's listed but deferred, load it by name via tool search.
- **Shell** (always works): `codegraph explore "<symbol names or question>"` prints the same output.

If there is no `.codegraph/` directory, skip CodeGraph entirely — indexing is the user's decision.
<!-- CODEGRAPH_END -->

<!-- BEGIN AQG rules (managed by scripts/install_aqg_rules.py; do not edit inside) -->
## Agent Quality Gates (AQG) engineering discipline

- Before writing, modifying, or refactoring code, invoke the `aqg-code-construction`
  skill and follow its 6 steps. Its step 5 is the audit-before-commit gate.

- **Blast radius outranks size.** A change touching auth, permissions, crypto,
  secrets, trust-boundary input, data model, CI/deploy, install integrity,
  anything irreversible, or cross-repo contracts is `deep` — no matter how few
  lines it touches.

- **Trivial and non-sensitive** — a rename, a reformat, a comment, or anything a
  test / type-check / lint fully settles — is **NOT audited**. Audit is the
  exception, not the reflex. At most ONE audit per logical change.

- The other `aqg-*` skills announce their own triggers; invoke them by those.

- When delegating to a cold-started agent (sub-task, cron, remote, headless), write
  the discipline into the prompt: it inherits none of this context, and where
  `AQG_ROOT` is unset every AQG hook silently no-ops.

- Full ladder and the authoritative sensitivity list:
  /Users/tai/.deeppattern/agent-quality-gates/docs/policies/audit-trigger.md
<!-- END AQG rules -->

# opencode auto-mode
At the start of every user request that involves writing, editing, or fixing code:
1. Run `test -f ~/.local/share/opencode-auto.flag` (silent, no output to user).
2. If the flag exists → automatically invoke the `opencode` skill exactly as if the user had typed `/opencode <their full instruction>`. Do NOT ask first, do NOT explain — just delegate.
3. If the flag is absent → proceed normally.

The flag is toggled by `/opencodeon` and `/opencodeoff`.

# Tools instructions

Scope: Admin `tools/` and Development Space `repos/`. Development Space owns
product source under `~/development-space/repos/<tool-name>/`. Admin is a user.

## Use a tool

1. Read the tool's own `README.md` and run it as documented.
2. Prefer the stable checkout. Leave its source files unchanged unless you are
   doing an approved local fix.

## When a tool fails or needs a change

1. Reproduce the problem and capture the command, output, and tool revision (`git -C <tool> rev-parse HEAD`).
2. Search the tool's open issues. If one matches, add your evidence to it as a comment.
3. Otherwise draft one issue for the problem that blocks you: what you ran, what happened, what you expected, the revision.
4. After Tai approves, file it with `gh issue create --repo <owner>/<repo>`. Report the issue URL.
5. Local fixes for Development Space–owned tools happen under
   `~/development-space/repos/<tool-name>/`, following `~/development-space/AGENTS.md`.

Admin does not create workshop automation or revive retired tools
(`automation-incidents`, `opencode-free-router`).

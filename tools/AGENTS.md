# Tools instructions

Scope: `tools/`. Development Space owns every tool. Admin is a user.

## Use a tool

1. Read the tool's own `README.md` and run it as documented.
2. Use the stable checkout. Leave its source files unchanged.

## When a tool fails or needs a change

1. Reproduce the problem and capture the command, output, and tool revision (`git -C <tool> rev-parse HEAD`).
2. Search the tool's open issues with the `github` skill. If one matches, add your evidence to it as a comment.
3. Otherwise draft one issue for the problem that blocks you: what you ran, what happened, what you expected, the revision.
4. After Tai approves, file it with `gh issue create --repo <owner>/<repo>`. Report the issue URL.
5. If the tool has no remote yet, give Tai the draft and note that the tool still needs migration to Development Space.

Fixes happen in Development Space, following `~/development-space/AGENTS.md`. Admin does not edit tool source, create tool branches, or create tool worktrees.

# Batch 2: independent tool repositories

Request: 009. Executed 2026-10-23. Parent base `40e9d38…`.

## Result

| Tool | Repository | Branch | First commit | Tracked files | Remote |
| --- | --- | --- | --- | --- | --- |
| OpenCode Free Router | `~/.agents/tools/opencode-free-router/` | `main` | `21cb19c8251152e90b1b04c0e6a4fde8781581ec` | 39 | None |
| Hindsight | `~/.agents/tools/hindsight/` | `main` | `ea0c7e9772568ac0901e675a7457476621a9c2af` | 4 | None |

Each repository carries a `PROVENANCE.md` naming the parent repository, the base
revision, the parent path, the recovery command, and the excluded runtime state.

## Admin index transition

| Step | Command | Observed |
| --- | --- | --- |
| Record the tracked set | `git ls-files tools` | 42 paths |
| Record content hashes | `git ls-files -z tools \| xargs -0 shasum -a 256` | `evidence/tools-index-before.sha256` |
| Add the boundary | append `/tools/` to `.gitignore` | Rule present |
| Remove index entries only | `git rm -r --cached tools` | 42 staged deletions, 0 removals on disk |
| Confirm empty index | `git ls-files tools \| wc -l` | `0` |
| Confirm working files | per-path existence check | All 42 present |
| Confirm the rule | `git check-ignore --no-index` | Both sampled paths match `/tools/` |

`tools/README.md` was the Admin-side index of the two tools. Its content moved to
`docs/tools.md` and the file was deleted from disk, because the ignore rule makes
a tracked Admin index inside `tools/` impossible. The deletion is recoverable at
`40e9d38:tools/README.md`.

## Worktree registration for request 008

| Field | Value |
| --- | --- |
| Repository | `/Users/tai/.agents/tools/opencode-free-router` |
| Base | `main` at `21cb19c8251152e90b1b04c0e6a4fde8781581ec` |
| Branch | `admin/opencode-free-router_008` |
| Worktree | `/Users/tai/development-space/worktrees/admin/opencode-free-router_008` |
| Registration | Listed by `worktree list --porcelain` with the same HEAD |
| Development Space Git | Ignores the path via `.gitignore:2` (`worktrees/`) |

## Excluded runtime state

`model-list.json`, `.model-sync.lock`, and `.quality-cache/` were already ignored
by the tool's own `.gitignore`. `__pycache__/`, `*.py[cod]`, `.pytest_cache/`,
and `.DS_Store` were added. All remain on disk, untouched.

## Secret scan

Pattern scan for provider tokens, CLI tokens, GitHub tokens, and `api_key`
assignments across both tool trees returned no matches. No credentials were
found in tracked source.

## Not done

- No remote was added, no repository was published, no parent history was
  rewritten.
- No submodule or gitlink was introduced. The Admin index holds no entry under
  `tools/`.

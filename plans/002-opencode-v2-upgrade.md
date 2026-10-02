# Plan 002: Upgrade OpenCode from V1 to V2 and refresh the affected baselines

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving on. If
> anything in the "STOP conditions" section occurs, stop and report; do not
> improvise. Update this file's status row in `/Users/tai/.agents/plans/README.md`
> when done.
>
> **Drift check (run first)**:
> `opencode --version` → `1.18.34`;
> `shasum -a 256 /Users/tai/.config/opencode/opencode.jsonc` →
> `e23193d5da7279547eb81470d4cb24b7d0844d361457861c89477a06ea9c4c81`.
> On a mismatch, STOP and report what changed instead of proceeding.

## Status

- **Priority**: P1
- **Effort**: M
- **Risk**: MED (replaces a machine-wide binary the operator's workflows depend on)
- **Depends on**: none; precedes GI-002 Stage C refresh and all Stage D evaluation work
- **Category**: migration / dx
- **Planned at**: 2026-10-02, no commit SHA
- **Operator approval**: granted 2026-10-02, with two recorded decisions: the quota plugin may be dropped ("bỏ qua luôn cũng được"), and the operator's stated worry is re-authentication after the upgrade

## Why this matters

The installed OpenCode is V1 (`1.18.34`, Homebrew tap `anomalyco/tap`). V2 is
required by the operator's decisions of 2026-10-02: the top-level
`websearch.provider` setting only activates in V2, V2 removes the documented
CLAUDE.md fallback (which simplifies GI-002's fallback-migration section to a
plain `~/.config/opencode/AGENTS.md`), and plan GI-001/GI-002 Stage D evidence
must be produced against whichever binary will actually be used afterward.
Upgrading first avoids re-running evaluations.

## Operator worry recorded for explicit verification

Auth. The installer replaces the binary only. Credentials live in
`~/.local/share/opencode/auth.json` (mode 600, one OpenAI oauth credential as
of 2026-10-02), outside config and outside Homebrew, and the V1→V2 migration
guide lists no auth break. Step 5 below verifies this concretely before
anything else is trusted.

## Current state

- Binary: `/opt/homebrew/bin/opencode`, V1 `1.18.34`, installed via Homebrew
  tap `anomalyco/tap` (brew's `opencode` stable is still 1.18.34, so
  `brew upgrade` does NOT produce V2; V2 comes from the V2 installer).
- `~/.config/opencode/opencode.jsonc` (live, hash `e23193d…`):

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": [
    "@slkiser/opencode-quota@4",
    "github:Silur/ponytail"
  ],
  "provider": {
    "openai": {},
    "opencode": {}
  },
  "websearch": {
    "provider": "random"
  }
}
```

- Plugin facts: the quota plugin is at npm `4.10.7` under tag `v4-latest` with
  `latest: 5.0.1` — the 5.x line is the likely V2 line, but V1 plugin
  implementations do not run in V2, so per the operator's decision the quota
  plugin is DROPPED from config rather than ported. The `github:Silur/ponytail`
  plugin has no verified V2 status; it is kept and its load is verified
  (Step 6), with report-and-decide if broken.
- Auth: `~/.local/share/opencode/auth.json` (do not print its contents; do not
  edit or delete it).
- The `websearch.provider: "random"` line was added by an unidentified tool
  between 2026-10-01 23:27 and 2026-10-02 14:38 (evaluation receipt
  `global-guidance-workspace/evaluation-results.md:30-31`); it is a valid V2
  setting and becomes live after this plan. It stays.
- Relay: `/Users/tai/.agents/skills/opencode-delegate/scripts/relay.mjs`
  drives `opencode run` via CLI only (no server API), so it should survive;
  Step 7 smoke-tests it.

## Commands you will need

| Purpose | Command | Expected on success |
|---|---|---|
| Current version | `opencode --version` | `1.18.34` before; `2.x` after |
| Config hash | `shasum -a 256 /Users/tai/.config/opencode/opencode.jsonc` | matches drift line above |
| Credential list | `opencode auth list` | shows the OpenAI credential, no login prompt |
| Live model check | `opencode run --model opencode-go/mimo-v2.6-flash 'Say hi'` | prints a greeting, exit 0 |
| Relay syntax | `node /Users/tai/.agents/skills/opencode-delegate/scripts/relay.mjs --help` | exit 0, help text |

## Scope

**In scope** (the only changes this plan makes):
- `/Users/tai/.config/opencode/opencode.jsonc` — remove the
  `"@slkiser/opencode-quota@4"` entry from the `plugin` array; keep
  `github:Silur/ponytail`, the two `provider` declarations, and the
  `websearch` block untouched.
- Backup copies under `/Users/tai/.agents/plans/002-opencode-v2-upgrade-workspace/`.
- The Homebrew V1 package removal and the V2 installation the operator approved.

**Out of scope** (do NOT touch):
- `~/.local/share/opencode/auth.json` and any credential store contents.
- Any other key in `opencode.jsonc` (the empty `provider` declarations stay).
- The GI-001/GI-002 plan or candidate files (GI-002 refresh happens after this
  plan as its own step; this plan only records the effects).
- Claude/Codex/Cursor setups, skills, `~/.agents` contents, model credentials
  or provider configuration elsewhere.
- No `opencode service restart`, no `opencode serve`, no `opencode upgrade`
  invocation (V2 is installed by the installer itself).

## Steps

### Step 1: Record and back up the pre-state

```bash
opencode --version
shasum -a 256 /Users/tai/.config/opencode/opencode.jsonc
mkdir -p /Users/tai/.agents/plans/002-opencode-v2-upgrade-workspace
cp /Users/tai/.config/opencode/opencode.jsonc \
   /Users/tai/.agents/plans/002-opencode-v2-upgrade-workspace/opencode.jsonc.pre-v2
opencode auth list | head -8
```

Record all outputs in the workspace as `pre-state.txt`. Copying the config is
a file copy only; the credential file is never copied or printed.

**Verify**: `opencode --version` prints `1.18.34`; the config hash matches the
drift line; `pre-state.txt` exists and lists one OpenAI credential.

### Step 2: Drop the quota plugin from config

Edit `/Users/tai/.config/opencode/opencode.jsonc` so the `plugin` array
contains only `"github:Silur/ponytail"`, preserving every other byte.

**Verify**: `shasum -a 256 ...` changes; `cat` shows `"plugin": [ "github:Silur/ponytail" ]` and the untouched provider/websearch blocks; the backup copy still matches the pre-state hash.

### Step 3: Remove V1 and install V2

1. `brew uninstall opencode` (the tap package only).
2. Fetch `https://opencode.ai/v2/docs/cli` and follow its documented install
   path for the V2 terminal client verbatim; do not guess flags. Record the
   exact command used in the workspace.
3. Do not restart any background service; binary replacement is the whole
   operation.

**Verify**: `command -v opencode` prints a non-Homebrew path (or the tap path
replaced); `opencode --version` prints a version whose major is `2` (match it
against the version the V2 docs name).

### Step 4: Confirm config loads with no breaking warnings

Run a harmless short call:

```bash
opencode run --model opencode-go/mimo-v2.6-flash 'Say hi'
```

**Verify**: greeting output, exit 0. If startup logs show config warnings
(unknown fields, malformed values), capture them into the workspace and
continue only if the warnings do not concern auth or the websearch block.

### Step 5: Verify the credential survived (the operator's worry)

```bash
opencode auth list | head -8
```

**Verify**: the previously recorded OpenAI credential still appears, with no
login requirement. NEVER print more of this output than the credential name
lines. If the list is empty or demands login, STOP — do not run
`opencode auth login` without the operator present.

### Step 6: Verify the kept plugin and the websearch setting

- Start one minimal `opencode` TUI check passively: grep the startup log for
  plugin load errors
  (`~/.local/share/opencode/log/opencode.log`, latest lines only) after the
  Step 4 run; record any ponytail failure verbatim (redact keys per improve
  Hard Rule 4 if any appear).
- Confirm the `websearch` block is accepted: rerun the Step 4 command and
  check the config warnings absent (captured in Step 4).

**Verify**: no unhandled startup error attributable to the ponytail plugin;
config warnings, if any, are filed into the workspace as `post-state.txt`.

### Step 7: Smoke-test the delegation path

```bash
node /Users/tai/.agents/skills/opencode-delegate/scripts/relay.mjs --help
```

**Verify**: exit 0 with help output. A full relay round-trip is NOT part of
this plan (it belongs to GI Stage D with its isolation gate); only syntax and
binary dispatch prove out here.

### Step 8: Record the result and hand the queue to the operator

Write `post-state.txt` (versions, hash, plugin outcome, relay outcome, warnings). Report: old → new version, auth continuity result, plugin status, and the two operator follow-ups — websearch keys (TUI `/connect` after upgrade, or a free Tavily key with no card at signup; Exa optional as second) and whether to keep `websearch.provider: "random"` now that it is live. Update the master index row to DONE.

## Test plan

Manual, per-step verification commands above. No automated tests exist for a
binary migration. The GI Stage D evaluation suite remains the real test of
V2 behavior and is explicitly out of scope here.

## Done criteria

Machine-checkable. ALL must hold:

- [ ] `opencode --version` prints a `2.x` version
- [ ] `opencode auth list` still shows the OpenAI credential (no login)
- [ ] `opencode run --model opencode-go/mimo-v2.6-flash 'Say hi'` exits 0
- [ ] `relay.mjs --help` exits 0
- [ ] `opencode.jsonc` plugin array contains exactly `"github:Silur/ponytail"`; backup exists in the workspace with the pre-state hash
- [ ] `pre-state.txt` and `post-state.txt` exist in the workspace, no secret values in either
- [ ] Master index row for this plan updated

## STOP conditions

Stop and report back (do not improvise) if:

- `opencode auth list` is empty or demands re-login (do not run
  `opencode auth login` without the operator present).
- The installer or `brew uninstall` fails twice after a reasonable retry.
- The ponytail plugin failure breaks startup outright (report; the operator
  decides drop/keep, since only the quota plugin was pre-approved to drop).
- V2 rejects the config in a way that blocks `opencode run` entirely.
- Tool calls from the running harness session begin failing mid-upgrade
  (finish the remaining steps by pasting the recorded commands into the
  operator's own terminal).
- Any secret value would need to be displayed or moved to complete a step.

## Maintenance notes

- After this plan lands, GI-002's "OpenCode V1 fallback migration" section
  collapses to creating `~/.config/opencode/AGENTS.md` (V2 does not read
  `~/.claude/CLAUDE.md`); plan GI-002 is updated separately, this plan does
  not edit it.
- The `websearch.provider: "random"` becomes genuinely effective; if a Tavily
  (first) and optionally Exa key are connected, random rotates among available
  providers on rate limits, per the V2 websearch guide.
- If the operator later wants the quota popup back, its 5.x line
  (`latest: 5.0.1`) is the candidate to evaluate against the V2 plugin API;
  until then this plan's removal is the state of record.
- Rollback path: `brew install opencode` from tap `anomalyco/tap` restores
  V1; restore the workspace config copy.

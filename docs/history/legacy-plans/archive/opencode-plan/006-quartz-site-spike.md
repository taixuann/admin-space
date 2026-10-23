# Plan 006 (spike): Quartz view-only site inside the AutoSci fork

> **Executor instructions**: This is a design/spike plan, not a
> build-everything plan. Investigate, prototype, and answer the open
> questions; end with a recommended build spec. Follow steps in order. If any
> STOP condition occurs, stop and report — do not improvise. When done, update
> the status row in `/Users/tai/.opencode/plan/README.md`.
>
> **Drift check (run first)**: Plan 005 must show DONE (fork exists, local
> `origin` → fork). In the fork's clone, `git log --oneline -1` on
> `autosci-codex` should be `feca5e0` (or newer if 005 reconciled — use the
> live tip, but confirm `git status` is clean before starting).

## Status

- **Priority**: P2
- **Effort**: M (spike; coarse estimate, may revise to S or L)
- **Risk**: MED (touches the fork's layout; mitigated by working on a spike branch)
- **Depends on**: 005
- **Category**: direction / spike
- **Planned at**: autosci `feca5e0`, 2026-10-02

## Why this matters

The operator wants a view-only rendered site of the AutoSci knowledge base
(`wiki/`: notes, papers, concepts, experiments). Quartz is the chosen
publisher. The key architectural decision — already taken in discussion — is
that the site lives **inside the fork** (content and renderer in one repo),
built fresh from stock quartz, rather than rendering cross-repo from
`research-projects/tools/`. This spike validates that setup and produces the
build spec: what gets published, how it builds, where it deploys.

## Current state

Facts established during planning (verify each before relying on it):

- Quartz v5, stock upstream, zero local customization: the monorepo checkout at
  `/Users/tai/workspace/research-projects/quartz` is `jackyzha0/quartz@ab346fa`
  ("feat(v5): add plugin system"), `git status` clean, `content/` empty.
  Its `package.json` (`v5.0.0`, `"type": "module"`): scripts include
  `quartz: ./quartz/bootstrap-cli.mjs` and `docs: npx quartz build --serve -d docs`;
  `engines: node >= 22, npm >= 10.9.2`. Local toolchain satisfies this
  (node v22.22.3, npm 10.9.8 — re-verify with `node --version`).
- The monorepo `quartz/` submodule is UNUSED (empty content). Do not move it;
  its removal is Step 4 of this plan, only after the new site builds.
- AutoSci content: `autosci/wiki/` holds `index.md` plus `notes/`, `papers/`,
  `concepts/`, `experiments/`, `foundations/`, `ideas/`, `canvases/`, `graph/`,
  and scratch dirs (`tmp/`, `discovered/`, `web/`). `autosci/docs/` holds
  operator/deployment docs.
- Quartz is MIT-licensed; vendoring/rebuilding from it inside the fork is fine.

## Commands you will need

| Purpose | Command | Expected on success |
|---|---|---|
| Toolchain | `node --version && npm --version` | node ≥ 22, npm ≥ 10.9.2 |
| Scaffold | per quartz v5 `getting-started` docs (`quartz/docs/getting-started`) | site dir created |
| Build | `npx quartz build` (or the v5 equivalent from the docs) | exit 0, HTML emitted |
| Serve check | `npx quartz build --serve` + `curl -s -o /dev/null -w '%{http_code}' localhost:<port>` | `200` |

## Scope

**In scope**:
- A spike branch in the fork (name: `spike/quartz-site`), containing: the fresh
  quartz scaffold (e.g. `site/`), a content mapping from `wiki/`, and a
  `SITE-SPEC.md` note with your findings + recommended build spec.
- The monorepo `/Users/tai/workspace/research-projects`: ONLY Step 4's submodule
  removal (`git rm quartz`, one commit). Nothing else.

**Out of scope**:
- Merging the spike branch to the fork's `main`/`autosci-codex` — recommendation only.
- Rewriting wiki content for quartz compatibility beyond 2–3 sample pages (if
  systematic incompatibilities appear, document them and STOP per below).
- GitHub Pages / deployment wiring — recommend, don't implement (needs operator's
  Pages/traffic decisions).
- `research-projects` beyond the quartz removal.

## Git workflow

- All site work on `spike/quartz-site` in the fork clone. Conventional commits.
- Never push to `skyllwt/AutoSci`; `origin` must be the fork (re-verify per 005).
- Do NOT push the spike branch unless the plan's verification needs remote CI —
  default is local-only; state which you chose in the report.

## Steps

### Step 1: Learn the v5 scaffold path (read-only)

In a THROWAWAY directory under `/private/tmp` (not in any repo), follow the
quartz v5 `getting-started` guide (`quartz/docs/getting-started` in the monorepo
checkout — read-only reference) to produce a hello-world site. Record: exact
commands used, Node/npm versions, build time, output dir layout.

**Verify**: `npx quartz build` (or documented v5 equivalent) exits 0 and emits
an `index.html` you can open. If the documented path fails twice on a clean
scaffold, STOP and report (v5 instability — do not debug upstream).

### Step 2: Spike inside the fork

On `spike/quartz-site` (branched from the fork's `autosci-codex` tip):

1. Add the quartz scaffold at `site/` (same method as Step 1).
2. Map content: point quartz's content dir at a COPY of 3–5 representative
   wiki pages (pick across `notes/`, `papers/`, `concepts/`), not a symlink
   (symlinks across the scaffold boundary behave inconsistently — verify or avoid).
3. Build. Record every incompatibility (wikilinks, canvases, dataview-style
   queries, non-ASCII paths) verbatim.

**Verify**: build exits 0 on the sample; incompatibility list written to
`site/SPIKE-NOTES.md` in the branch.

### Step 3: Write the build spec

Add `site/SITE-SPEC.md` (in the spike branch) answering:
1. Full content mapping: which `wiki/` subtrees publish, which are excluded
   (`tmp/`, `discovered/`, `web/` are suspects — justify each).
2. Copy vs symlink vs quartz-native content dir for the full wiki.
3. Build + deploy recommendation (local `build --serve` vs GitHub Pages vs other).
4. What the operator must decide (theme, public/private, custom domain).

### Step 4: Remove the dead monorepo submodule (only if Steps 1–3 succeed)

In `/Users/tai/workspace/research-projects`:
`git rm quartz` + commit `chore: drop unused quartz submodule (site now lives in AutoSci fork, see plan 006)`.
Then `git submodule status` must exit 0 (note: it currently ALSO fails on the
two broken `archived-projects/*` gitlinks — those are out of scope here; record
whether they still fail and say so in the report rather than fixing them).

## Test plan

- The spike's "tests" are the build gates above (clean scaffold build, sample
  content build) plus the monorepo `git submodule status` exit code recorded
  before/after Step 4.
- No unit tests; nothing in `Tests/` anywhere is touched.

## Done criteria

- [ ] `spike/quartz-site` exists in the fork with scaffold + 3–5 sample pages + `SPIKE-NOTES.md` + `SITE-SPEC.md`
- [ ] Sample build exits 0 (evidence: command output in report)
- [ ] Open questions in "Build spec" all answered or explicitly deferred to the operator
- [ ] Monorepo `quartz/` submodule removed by `git rm`, committed; `git status` clean otherwise
- [ ] Index status row updated

## STOP conditions

- Plan 005 not DONE (no writable fork).
- Clean quartz scaffold doesn't build (upstream v5 issue — report, don't fix upstream).
- Sample wiki pages need systematic rewrites for quartz (more than front-matter tweaks) — document and STOP; the content-mapping decision belongs to the operator.
- Anything requires touching `skyllwt/AutoSci` or editing wiki content beyond samples.

## Maintenance notes

- If quartz v5 changes its scaffold path, Steps 1–2 must be re-run; the spec's
  value is the content mapping + deploy answers, which survive that.
- Whoever implements the full site later starts from `spike/quartz-site` +
  `SITE-SPEC.md`, not from this plan.
- Reviewer focus: the exclusion list (publishing `tmp/`/`discovered/` by accident
  leaks scratch notes to a public site — check the mapping file-by-file).

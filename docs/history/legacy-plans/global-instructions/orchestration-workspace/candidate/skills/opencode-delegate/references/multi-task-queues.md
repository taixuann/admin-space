# Multi-task queues

The single-task loop scales to a queue, and that's where delegation pays off most — a removal split
across layers, a migration touching many files, a refactor sweep. The discipline that makes a queue
trustworthy is sequencing and bookkeeping, not parallelism.

## Run sequentially, land at the agreed boundary

Tasks stay **one at a time, in dependency order** — that part doesn't change. What changes is where
you land them:

- **Unrelated tasks** (separate goals, separate briefs): land each one — review + gates, plus
  whatever commit step the governing workflow authorizes — before dispatching the next.
- **One approved batch** (ordered, dependent steps inside a single authorized, coherent job): keep
  them in one brief and run them serially, each step's gate locally before the next step. You review
  the cumulative diff **once, at the batch boundary** — not after every microstep. The batch ends at
  its recorded checkpoint (human decision, protected transition, or required independent review),
  which closes this batch and requires a new dispatch. Proceed on to that next batch only if the
  current user request or governing task contract already records the authorization for it;
  otherwise wait for authorization. Don't ask again for authorization already on record.

Steps whose authorization, mutable scope, or review requirements differ are not one batch — they
stay separate briefs. There is no fixed task-count limit either way; compatibility is the test.

Why serial either way:

- **Later tasks assume earlier ones are in the tree.** Task 3's brief can say "the X added in the
  previous step exists" only because the previous step's changes are still there — verified and
  uncommitted, or committed if the governing workflow commits between units.
- **Landing per unit keeps history reviewable** and any single unit revertible — when commits are
  authorized at all. Under a read-only governing workflow (e.g. `improve`), nothing lands; the batch
  stays uncommitted and the review is the boundary.
- **Each review is honest.** A tree holding only the current unit's changes means the next task's
  `touchedFiles` shows *its* changes, not a pile-up from earlier work.

Parallelism is occasionally worth it for genuinely independent tasks on separate files, but it
sacrifices the clean-tree-per-unit property and makes review harder. Default to sequential. (Each fresh
`relay.mjs` dispatch starts a new OpenCode session, so independent tasks don't share context — fold any
shared constraint into each brief, see below.)

## Carry decided constraints forward

Implementation surfaces facts the original plan didn't have: a helper got named, a fixture lives in a
specific place, an interface was chosen. When a later task depends on one of those, **fold it into that
task's brief** as an explicit line. A fresh OpenCode session has no memory of the earlier run, so a
constraint that emerged in task 2 must be restated in task 5's brief or it won't hold. This is the queue
equivalent of keeping briefs self-contained.

## Keep a progress file

For anything longer than two or three tasks — especially a run the human steps away from — maintain a
single progress file alongside the work. It's the durable record that survives your own context limits
and lets the human catch up at a glance. A shape that works:

- **Status table** — each task: queued / at-implementer / reviewed (+ committed, with the commit hash, when the governing workflow authorizes commits).
- **Per-task review notes** — what landed, what you verified, the gate outcome. One short paragraph.
- **"Needs your eyes"** — design decisions OpenCode made, non-blocking nitpicks, anything you want the
  human to overrule or confirm. This is the section they read first.
- **End-of-run checklist** — what happens after the last task (push, open/update the PR, manual checks
  the human should do).

Update it as each task lands, not in a batch at the end — if the run is interrupted, the file is still
accurate.

## Close with a coherence check

Per-task review proves each step in isolation; it doesn't prove the steps cohere. After the last task,
verify the whole:

- Run the full test/build once more on the final tree — not just the last task's slice.
- Do a repo-wide check for the thing the queue was about (e.g. after a removal, grep the entire tree
  for any surviving reference; after a rename, confirm no stragglers).
- For schema work, replay all the new migrations from a clean state and check for drift.
- Then, if the governing workflow authorizes publication, push and open or update the PR, with a
  description that reflects what actually shipped. If it doesn't, stop at the review boundary and
  report: the diff, the gate results, and what remains uncommitted.

## When to stop and ask

Proceed without asking on anything that follows from the agreed plan — that's the point of the human
opting into the queue. Stop and surface when:

- A task can't be completed correctly within its brief's scope (a scope change is the human's call).
- A review finds something that calls the *plan* into question, not just the implementation.
- The gates reveal a problem that affects tasks already "done."
- A batch reaches a recorded checkpoint — a human decision or a required independent review. Stop
  there and report; the checkpoint ends this batch and requires a new dispatch, not a continuation of
  this one. Dispatch the next batch only if the current user request or governing task contract
  already covers it; if not, wait for authorization — and don't re-ask for authorization that is
  already on record.

Then report where you are, what has landed (or what is still uncommitted), and what the open
question is — and wait. A queue that quietly works around a broken assumption produces a lot of
commits in the wrong direction.

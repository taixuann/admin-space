---
name: brainstorming
description: Explore genuinely open research directions, map what is known and uncertain, and develop candidate questions for scientist selection. Use for open-ended ideation, research gaps, or choosing among directions. Do not use to reopen a settled descriptive question or settled methods; use plan-research for planning within a chosen scope.
allowed-tools: [Read, glob, grep, webfetch, research_search]
license: MIT
metadata:
  summary: "Map what is known, generate directions by named moves, and leave selection to the scientist."
  category: core
  role: workflow
  version: 1.0.0
  author: Synthetic Sciences
  upstream: K-Dense-AI/claude-scientific-writer
  upstream-url: https://github.com/K-Dense-AI/claude-scientific-writer
  upstream-path: skills/scientific-brainstorming
  upstream-license: MIT
  upstream-relationship: adapted and rewritten
  adapted-by: Synthetic Sciences
  skill-author: Synthetic Sciences
  adapted-from: K-Dense scientific-brainstorming and scientific-problem-selection (MIT)
---

# Brainstorming

Good research ideas are not found by asking for good ideas. They come from a clear map of
what is known, a deliberate set of moves that produce many candidates, and a cold ranking
that throws most of them away. Generation and selection are separate steps; mixing them
kills the unusual candidates first.

## Rules

1. **Map before you generate.** A brief map of what is established, contested and
   what is assumed produces better candidates than an hour of free association. Use the
   user's notes and, when the field is unfamiliar, one research-lookup or a shallow
   literature-review round.
2. **Generate a useful range, by named moves.** Scale the number of candidates to the
   scope and time available. Use the moves below when they fit; write each candidate as
   the change and outcome it would show. Do not judge while generating.
3. **Rank cold.** Score each candidate on value if it works, probability it works,
   cost to find out, and whether the user can do it with what they have. Prefer the
   candidate that is cheap to test and informative either way.
4. **Offer a shortlist**, sized to the choice at hand, with a first test and a result
   that would count against each direction. The scientist selects the direction.
5. **Say what is already done.** A candidate that exists in the literature is a lead to
   read, not an idea to pursue; mark it.

## Moves

| Move | Question that produces candidates |
| --- | --- |
| Gap | What does every paper assume, measure or exclude without justification? |
| Transfer | Which method from an adjacent field has never been applied here, and why not? |
| Inversion | What if the accepted direction of the effect, or the usual objective, is reversed? |
| Constraint | What changes under a tenth of the data, compute, labels, or time? Under ten times? |
| Failure | Where does the best method fail, and what is common to those cases? |
| Measurement | Is the standard metric measuring the thing everyone claims? What would? |
| Composition | Which two known results, combined, predict something neither does alone? |
| Mechanism | The effect is established; what is the mechanism, and what would distinguish candidates? |
| Simplification | What is the simplest baseline nobody reports, and would it match? |

`references/methods.md` expands these into structured exercises (SCAMPER, morphological
analysis, assumption reversal, analogical transfer) for a longer session.

## Workflow

- [ ] Map: established / contested / assumed / open, in a short table with sources.
- [ ] Generate: enough one-line candidates to expose meaningful alternatives; tag moves when useful.
- [ ] Filter: remove duplicates, the already-published, the untestable.
- [ ] Rank: value × probability ÷ cost, plus feasibility with the user's resources.
- [ ] Offer a focused shortlist with first test and counterevidence; hand the selected direction to planning.

## Selection criteria

- **Value**: who changes what they do if this is true? A result nobody would act on is low
  value however elegant.
- **Probability**: is there a mechanism or prior evidence that makes it plausible, or is it
  a hope?
- **Cost**: the cheapest experiment that would move the probability substantially; hours
  versus months.
- **Informativeness**: does a negative result teach something? Prefer questions where
  both answers matter.
- **Fit**: the user's data, compute, skills and deadline. A perfect idea for someone else
  is not on the shortlist.

## Deliverable

```markdown
## Map
| Established | Contested | Assumed | Open |

## Candidates (by move)
1. [gap] ...   2. [transfer] ...   ...

## Shortlist
1. <idea>. First experiment: <...>. Killed if: <...>. Value / probability / cost: <...>.
2. ...
3. ...

## Already done (read these)
- <candidate> → <paper, link>
```

## Before you hand it over

- The map cites its sources or says it comes from the user's notes.
- Candidates span at least four moves; none is a restatement of another.
- Each shortlisted idea has a concrete first experiment and a kill criterion.

## Handoff & Next Steps

When the shortlist is delivered and the scientist selects an idea to pursue:
- Hand off to [Plan Research](../plan-research/SKILL.md) to draft the study plan. Use [Ask Einstein](../ask-einstein/SKILL.md) for bounded, read-only consultation on unresolved research questions or constraints.
- See [state transitions](../../references/transitions.md) for full lifecycle details.

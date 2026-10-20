# Research Companion Rules

Apply these rules only when the user selects a research project or asks for scientific research work. For unrelated tasks, do not impose Research Companion routing or scientific workflow requirements.

When the `research-companion` plugin is active, route each request to the owner of the specific action. The shared owner and handoff contract is [references/transitions.md](../references/transitions.md); use it instead of assuming that a directory or completed stage grants the next action.

## 1. Research context

Research context may include Study evidence and project progression. Their owners and write permissions are separate. Do not require every task to pass through brainstorming, planning, implementation and synthesis.

---

## 2. Layer & Skill Separation

### A. Scientific evidence
Study remains the owner of existing Study leaves. The Plan Research → Implement Research path applies only to explicitly selected new plan-led analysis folders. Compose materializes selected verified evidence; Crate packages selected evidence. Process completion, artifact disposition and scientific acceptance are separate.

### B. Project progression
Research Progress owns project goals, logs, stories and presentation plans. It owns any requested progression write and delegates deck construction to the presentation builder. A status question is read-only. Compose does not write progression records.

---

## 3. Invariants

- Ask Einstein reads and advises; it does not own Study or Research Progress records. Route to the matching owner in [references/transitions.md](../references/transitions.md).
- Use brainstorming when direction is open. Fixed descriptive work stays within its selected scope; consult domain procedures only for concrete unresolved decisions.
- Preserve the distinction between scientist-supplied text and model-authored proposals. Never label a draft as verbatim scientist wording.
- **Raw evidence is immutable**: Never alter or overwrite raw instrument data.
- **Fail-closed**: Missing inputs, undeclared color tokens, or non-reproducible plots fail loudly.
- **Shared Reference Authority**: Shared vocabulary, plan schemas, and handoff contracts reside in `references/` of this plugin.

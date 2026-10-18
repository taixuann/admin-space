# Companion

Personal plugin with eight workflows: init, ask, document, organize, plan, apply, capture and weekly review. Shared definitions and Simple English are internal references.

Plan produces one self-contained local HTML proposal with retrieval metadata through the installed `answer-me-with-html` skill. The renderer uses a temporary Markdown draft and embeds it in the HTML; no separate Markdown plan file is saved. Organize reviews project Notes and Resources before handing a concrete proposal to Plan.

Init Companion resolves the selected workspace, reads applicable ancestor and nested instructions, and hands the task to its owning workflow. It performs read-only orientation and preserves existing authorization.

Document Companion follows local collection READMEs for file organization and naming. Ask routes local document requests to it while preserving the read-only discussion boundary.

Notion is required for project records, but not for local-only document work. Use existing GitHub and Exa connections only when relevant. No connector credentials or custom MCP servers are bundled. Two shared priority references point to the owner’s Notion workspace.

Source: `~/.agents/plugins/companion`. Install from the Personal Companion marketplace and start a new chat. Refresh or reinstall the plugin after source changes because the host loads a cached copy.

English guidance is vendored from AminBlg/SimpleEnglish under MIT. See shared/writing/simple-english/PROVENANCE.md and LICENSE.

## Updating the uploaded copy

Edit this source, validate the relative links and workflow boundaries, and increase the version in both manifests. Package the plugin with `.codex-plugin/plugin.json`, `skills/`, and `shared/`. Update the existing uploaded Companion entry so it keeps its identity; do not install another marketplace copy. Verify the new version in a fresh chat before removing a workspace-local skill copy.

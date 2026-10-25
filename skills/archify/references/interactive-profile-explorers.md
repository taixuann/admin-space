# Interactive profile explorers

Use when a reader needs to explore an agent's workflow, capability dependencies, identity, memory, and operating boundaries together.

## Establish the artifact contract

For this user, a unified explorer is one HTML document with one connected primary diagram surface. Workflow stages and their supporting capabilities share that graph. Identity, memory, environment, and authority constrain the same journey. A wrapper containing separate workflow and environment pages, including inline srcdoc pages, is a different interface even when downloadable as one file.

Separate interface shape from storage. Keep the visible profile entrypoint and documents clean; place builder scripts, authored mapping, diagram sources, and receipts together in one hidden .archify bundle. A profile-local bundle or a relative symlink to one root bundle provides the same inspectable ownership. Use one actual source, not copied bundles. Preserve compatibility links when existing consumers depend on old paths.

## Choose the requested scope

For a workflow-only preview, select the native mode from the question: Workflow for responsibility handoffs; Lifecycle for request states, readiness, waits and retries. Preserve one workflow HTML when the user asks for a clearer state machine instead of creating another public view. Add capability expansion or availability switches only when requested. A simpler workflow replacing an explorer does not need to inherit its interaction framework, because that would preserve complexity the reader explicitly removed. Apply the Secretary model in SKILL.md rather than turning every supporting method into another work type.

## State-and-artifact recipe

1. Identify the object whose state changes: one management request, not the entire fleet's live health. Select the target profile and operation inside that lifecycle. Keep the user-facing HTML name stable when changing the native diagram mode.
2. Establish states and tangible outputs before drawing roles. A profile-management path is Draft, Defined, Planned, Executing, Verifying, Done. Attach an owner and artifact to each: requirements; maintained profile definition; executable plan; scoped changes and test results; saved/runtime evidence; reconciled definition, plan status and report. Name real owning artifact paths, not a new manifest duplicating them.
3. Add transition guards and alternative endings. Definition-only authorization ends without deployment. Execution requires the approved plan, verified worker readiness and the task's authorized access. Give every recoverable wait a resume event. Send failed verification through plan revision before retry. Do not imply that every request must traverse all lifecycle states or every fleet-admin action.
4. Connect capability selection to actual activation. Describe skills selection, discovery/loading and fresh-session verification; plugin installation/enabling/configuration and hook checks; profile-scoped MCP setup, required user authorization and a real tool check. Keep credentials outside documentation. For scoped automation changes, name the trigger, runner, side effects, recovery and actual test; for memory, distinguish target bank from tested access and health. Link native specialist procedures instead of inventing setting names or activation commands.
5. Show prerequisites without circular execution. Complete the worker's own definition, approved setup and readiness checks through the existing approved runner before assigning it configuration tasks. A documented worker is not a running executor. Keep preparation and authorized application distinguishable according to the current execution contract; naming a configuration task grants no additional permissions.
6. Author native Lifecycle schema v3 with every consecutive mainPath transition explicit. Keep state labels and transition guards concise. Put complete artifact contracts and longer transition explanations in cards explicitly associated with those states or transitions; retain the decisive condition on the arrow.
7. Finalize the candidate through the installed entrypoint: `node <archify-cli> finalize lifecycle <candidate.json> <canonical.html> --quality showcase --out-dir <fresh-evidence-dir> --json`. If the native type changes at an existing public path, preserve the previous source/artifact/evidence first and update the maintained source pointer and rebuild command together. Old receipts cannot certify the new diagram.
8. On `lifecycle/too-wide`, inspect `wideStepLabels`, `widthDriver` and spacing evidence before editing. Long transition notes expand main-path gaps. Move complete explanations to transition-associated cards and shorten the display wording while preserving the condition; do not shrink text, weaken gates or split a single requested workflow merely to fit. Re-finalize after repair.
9. Verify semantic coverage as well as rendering: main-path adjacency, approval/readiness guards, wait/resume events, rework-to-plan, documentation-only exit, artifact ownership and selection-versus-activation distinctions. Keep automatic browser acceptance separate from perceptual review. Report automatic crossover advice without removing required transitions or claiming visual polish that was not inspected.

## Promote a reviewed workflow

1. Inspect the approved folder contract, public links, canonical bundle and legacy builder/test destinations. Preserve identity sources and runtime links; packaging does not authorize runtime changes.
2. Save the retired HTML in the hidden archive. Compare source and archive bytes immediately before removing the old public entry, because concurrent edits must remain recoverable.
3. Put the maintained workflow candidate and canonical HTML in the owned hidden bundle. A relative public HTML symlink can expose the self-contained artifact without copying its build support into the visible folder.
4. Update the candidate's durable output path and run native `finalize` against the canonical HTML. Keep sidecars with that artifact. Preserve old receipts as history; use a fresh evidence directory after any browser-checked revision.
5. Update navigation, rebuild instructions, default writer destinations and browser fixture paths together. Keep legacy tools clearly separate from the current workflow generator so their next invocation cannot restore the retired public filename.
6. Verify the exact visible file set, relative link resolution, public/canonical artifact hash, memory and heading anchors, local links and unchanged identity. Run the writer-destination regression and relevant browser checks. Report filesystem/artifact acceptance separately from profile deployment.

## Build a full interactive explorer

1. Read the owning profile instructions, README, capability manifest, and work/permission rules. Establish which statements are desired targets, observed configuration, or verified behavior. Keep one capability inventory; credentials and full runtime configuration stay outside the view.
2. Author the single main graph before styling or packaging. Show request, context inspection, optional brainstorming and planning, direct work or delegated implementation, verification, and reporting. Connect capabilities to their supported stages. Draw conditions and alternate paths rather than making every skill mandatory.
3. Derive individual capability entries from the manifest. Validate every authored dependency ID against that inventory. Use strict duplicate-key loading for manifest and mapping because silent overwrites can change preview meaning. Keep plugin support distinct from skill invocation and actual execution tracing.
4. Integrate environment and authority into that same model. Include active identity source and any snapshot or runtime link, working directory, scoped read/write locations, read-only locations, bounded exceptions, and human approval gates. Show desired memory provider/bank separately from observed connectivity. Capability selection does not generate SOUL or relax permission rules.
5. Inspect native viewer controls before implementing new interaction. Author and finalize one native Archify baseline for the unified model. Integrate that actual graph into the final document; a separate checked baseline cannot certify a replacement SVG. Share stable node and edge IDs between the native graph, authored dependency mapping, and controls. Validate that every required stage and capability is present, including optional skill-authoring or automation branches, because a working switch can otherwise target a node the reader never sees. Use existing focus, search, and detail behavior where it fits. Preserve one graph rather than splitting the model into convenient diagram pages.
6. Implement expansion and availability preview as separate interactions in the same document. Expansion reveals a capability's purpose and supported stages. Preview switches highlight only its exact authored dependent nodes in the primary graph and name the disabled inputs. Describe unmodeled replacement as not assessed. Use 'No disabled mapped dependencies (preview)' rather than 'Active' to avoid implying runtime health.
7. Make reset restore all preview selections. Keep selections ephemeral: no YAML writes, localStorage, runtime settings, or backend changes. Identity, approval gates, and unresolved memory warnings remain visible and unchanged by every switch. Escape data in HTML and script contexts and use textContent for status updates.
8. If custom controls alter the finalized native HTML, preserve the exact baseline and receipts in the build bundle. Treat the final integrated page as a derived artifact with its own byte identity and independent browser assertions. Do not attach a native receipt to bytes it did not validate. Do not modify the shared Archify package merely to implement a profile-specific interaction.
9. Rebuild through the existing owner entrypoint, then verify the final document. Link its view, build command, and hidden support bundle from the profile README. Add watching or scheduling only when explicitly authorized; YAML-backed documentation does not require a running service.

## Focused proof

Use the owning test runner for schema and dependency tests. Cover missing and unknown IDs, duplicate keys, empty categories, malicious display strings, and preservation of the last good output after invalid input.

Run durable browser assertions, not print-only smoke checks:

- Copy the final HTML alone into managed scratch and open it through file://.
- Assert one primary graph and no iframe, srcdoc, object, embed, or nested HTML-page dependency.
- Assert that the workflow, individual capability support, identity, memory, and authority are represented in the connected model rather than split across separate diagrams. Compare final node and edge identities with the finalized baseline and current manifest/mapping; counting one SVG or one primary-graph element is not sufficient proof of semantic coverage.
- Collapse and expand capability details with pointer and keyboard.
- Disable a selected capability and assert the exact affected node set in the primary graph; unrelated nodes and permission text remain unchanged.
- Disable memory support while keeping the distinction between preview selection and actual memory health visible.
- Reset with pointer and keyboard; assert all switches and node statuses are restored.
- Check desktop and narrow widths in light and dark modes. Assert no horizontal overflow and inspect computed background/text colors; later light rules can override earlier dark rules. Inspect a real screenshot for readable labels, route congestion, toolbar overlap, and conditional branch meaning, because passing counters and viewport bounds can still hide an unusable graph. Keep optional brainstorming and planning paths visibly conditional, with a direct-work path that does not imply mandatory delegation.
- Inject an HTML-like label through a managed scratch fixture. Assert text display, no executable element, and no dialog.
- Assert no page errors, runtime-changing requests, or persistent preview writes.
- Verify that rebuilds preserve the agreed visible profile files and the hidden bundle link instead of scattering support outputs.

Use an installed browser or the renderer's successful executable path. Resolve it through the browser library or a bounded platform-path check before widening discovery. Reuse a confirmed executablePath when package and browser-cache versions differ. Do not install a browser without authorization.

## Evidence and handoff

Keep native baseline finalization evidence distinct from the final integrated page's interaction evidence and checksum. A relocation preserves bytes but does not refresh receipt paths or provenance. Retain historical receipts rather than rewriting them to imply fresh verification.

Deliver the final profile page with a short description of its two interactions and the statement that runtime settings and permissions are unchanged. Keep commands and detailed receipts in the owning build documentation. Describe only tests actually run; pending integration work is not a validated recipe.

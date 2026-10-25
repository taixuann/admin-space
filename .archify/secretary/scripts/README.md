# Profile capabilities renderer

Render `docs/profiles/<name>/capabilities.yaml` into `docs/profiles/<name>/capabilities.html` using Archify.

Secretary keeps only four profile files. Its legacy inventory output now goes to `.archify/profile-capabilities-secretary/capabilities.html`, not the profile folder. Its current `profile.html` embeds both native diagrams from `.archify/secretary-profile-support/`. That directory also preserves relocated outputs and receipts; receipt paths refer to their original publication locations and are historical evidence.

## Usage

Render both profiles:

```sh
python3 automation/profile-capabilities/profile_capabilities.py --once
```

Render one profile:

```sh
python3 automation/profile-capabilities/profile_capabilities.py --profile secretary --once
```

Watch for YAML changes and rebuild in the foreground:

```sh
python3 automation/profile-capabilities/profile_capabilities.py --watch
```

Stop the watcher with Ctrl-C. It is not a scheduled job or server. After a rebuild, reopen or reload the HTML file; there is no live browser push.

## Contract

- YAML is treated as untrusted data: schema, types, and duplicate keys are validated.
- Unsupported sections or unsafe Markdown directive injection are rejected.
- Generated candidates and receipts are written under `.archify/profile-capabilities-<name>/`.
- Invalid YAML or a failed render leaves the last successful HTML unchanged.
- The script exits nonzero on build failure.

## Secretary explorer

Rebuild the Secretary wrapper after changing its YAML or mapping:

The approved capability list stays in `docs/profiles/secretary/capabilities.yaml`. The authored workflow mapping lives at `automation/profile-capabilities/workflow-mapping.yaml`. Native diagram sources and archived receipts remain under `.archify/`; no extra diagram or evidence files belong in the Secretary profile folder.

```sh
python3 automation/profile-capabilities/secretary_explorer.py
```

Run durable browser assertions (uses the installed Playwright package and Google Chrome; no installation):

```sh
node automation/profile-capabilities/test_secretary_explorer_browser.cjs
```
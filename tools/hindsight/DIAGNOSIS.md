# Hindsight ingestion diagnosis

Observed: 2026-10-22.

## Findings

The backend API is reachable. Its running worker reports extraction failures through the `claude-code` provider.
The profile file `~/.hindsight/profiles/coding-agent.env` sets:

```text
HINDSIGHT_API_LLM_PROVIDER=claude-code
HINDSIGHT_API_LLM_MODEL=gemini-3.8-flash
```

The backend log reports both:

```text
Claude Code authentication failed: Not logged in · Please run /login
[claude-code:unrecognized_model] {"model":"gemini-3.8-flash","query_source":"sdk"}
```

Failed `batch_retain` tasks and retries appear in `~/.hindsight/profiles/coding-agent.log`.
This establishes an extraction failure, not a UI-only display issue.
The shared backend can affect multiple banks that use this provider. Each bank still needs its own state check.

## Next repair boundary

Choose a compatible provider and model together, and verify the credentials available to the daemon.
Restart only the affected backend through its native lifecycle.
Then verify one bounded retain operation reaches completion and recall returns its content.
Inspect failed operations before deciding which historical inputs to retry.

No provider, credentials, pending operations, or existing bank data changed in this diagnosis.
The installed OpenCode Free Router is a plugin, not a drop-in HTTP provider for Hindsight.

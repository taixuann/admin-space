# Delete a bot

Purpose: retire a bot safely. Deletion is reversible until Tai confirms the final removal of its folder.

Parent: [Harvey](../SOUL.md) · Shared rules: [bot folders](../../../AGENTS.md)

## Uses

- Skill: `hermes-fleet-admin`. Actions: Inspect, Configure, Verify.
- Model category: `operation.high`. Dependency checks and approved removal are routine work.
- Worker: Harvey, only for the step Tai approved in chat.

## Steps

1. Find dependencies. Search for the bot's name in:
   - scheduled jobs (`hermes cron list`);
   - gateway routes;
   - other bots' workflows under `~/.agents/bots/*/workflows/`.
   Completion: a list of each dependency, or an explicit "none found" from each search.
2. Report the dependencies to Tai. Ask for explicit confirmation of the deletion. Silence is not confirmation.
3. Back up the whole Hermes profile, `.env` included, to `~/.hermes/backups-admin/<bot>-<timestamp>/`, outside the profile and outside the repo. Create that folder with owner-only permissions. Never print `.env` values.
   Completion: the backup folder exists and holds the profile's files.
4. Run `hermes profile delete --help` to read the flags. Then remove the profile with the approved flags.
   Completion: the command exited 0.
5. Set `enable: false` in the bot's `SOUL.md`. Keep the folder as history.
6. Verify. The profile no longer appears in `hermes profile list`. No dependency from step 1 still points to it. Report each result.
7. Removing the bot folder is a separate step. Do it only when Tai confirms it.

## Error recovery

- A dependency exists: stop and report it. Do not remove the profile.
- The backup fails: stop. Do not remove the profile.
- The removal command fails: report the output. Do not retry without Tai.
- Verify fails: report the remaining reference to Tai.

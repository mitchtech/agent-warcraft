# Changelog

## 0.1.0 - 2026-10-21

First release, built on the Agent Johnny 5 v0.1.0 runtime.

- Play 56 *Warcraft III* lines for Claude Code, Codex, and Gemini CLI, plus a generic `play` interface for other agents.
- Map session start to "Ready to work.", prompts to "Work, work." and the other peon acknowledgements, approvals to "What you want?", questions to "Hmmm?", idle notifications to "Something need doing?", and finished turns to "Work complete!" (on by default).
- Add a `faction` setting: `horde` (orc peon, grunt, and advisor; the default), `alliance` (human peasant, footman, and knight: "Job's done!", "More gold is required."), or `both`. Every default cue has lines for both factions.
- Play "We need more gold!" when Claude Code stops on `rate_limit`, `billing_error`, or `account_on_hold`, or when a usage-limit wait ends without resuming, and "We need more lumber." on `max_output_tokens`. Other API errors keep the optional `error` cue.
- Add `agent-warcraft statusline`, a gold meter for Claude Code's status line that reads the 5-hour, 7-day, and spend-limit percentages and an optional per-session dollar budget. It warns once per session with "Our gold mine is running low." and plays "We need more gold!" at 100%.
- Play the peon's annoyed lines ("Me busy. Leave me alone!", "Me not that kind of orc!") on the third prompt sent within ten seconds. Only timestamps are stored.
- Play "We're under attack!" or "Our town is under attack!" when an approval's command is destructive (`rm -rf`, force push, `git reset --hard`, `DROP TABLE`, and similar). Only a yes/no flag leaves the hook; the command is never stored.
- Add optional `subagent_started` (Claude and Codex `SubagentStart`: "Zug zug."), `tool_failed` (Claude `PostToolUseFailure`: "Can't build there."), `context_compacting` ("Inventory is full."), and `session_ended` cues.
- Add a 2% easter egg ("For the Horde!", "For Lordaeron!") limited to non-urgent cues, with `mute easter-egg`.
- Record every clip's source URL, archive member, faction, and output hash in `audio/sources.json`, with a reproducible ffmpeg build and an offline `--check`; clips are loudness-matched at -16 LUFS and were checked against speech-to-text transcripts.
- Ship the Codex pet installer, validation, and packaging with a manifest-only Peon stub; `pet status` reports `not-bundled` until the art lands.
- Add a WC3-styled site with a clickable unit portrait that gets annoyed, a hotkey command card, a demo gold economy, and Horde/Alliance palettes.

# Changelog

## 0.3.0 - 2026-10-22

Meet the Peasant: the Alliance counterpart to the Peon, as a second native Codex pet.

- Add the human Peasant v2 pet with nine animations, sixteen look directions, original source art, lossless local and web atlases, and CC BY 4.0 contributor licensing.
- Package a dedicated Peasant ZIP, validate both pets and web exports, and derive Peasant previews from the active atlas.
- Attach `agent-warcraft-peasant-pet.zip` and `agent-warcraft-peasant-pet-web.webp` to releases.
- Add `agent-warcraft pet install peasant`. `pet status`, `pet uninstall`, and `doctor --pet` take the same optional pet name; without one they target the Peon, as before. Both pets install side by side.
- Show the Peasant on the site: the Alliance hero portrait acts out each cue with his animations, the pet section switches between the Peon and the Peasant (following the faction toggle), and the install commands and web atlases follow the chosen pet.
- Add Peasant previews to the README, Peasant scenes to `pet-preview.mp4` and `faction-preview.mp4`, and both workers to the banner and social card.

## 0.2.0 - 2026-10-21

Meet the Peon: a native custom pet for Codex desktop and Codex CLI.

- Bundle the Peon v2 pet with nine animations and sixteen look directions, preserve the original PNG, and record lossless WebP provenance and artwork licensing (CC BY 4.0).
- Attach `agent-warcraft-pet.zip` to releases for installation without Node.js, alongside the existing `agent-warcraft pet install`.
- Add a nine-row web atlas, `agent-warcraft-pet-web.webp`, for ChatGPT/Codex web pet uploads. `scripts/check-pet.py` verifies its pixels against the active atlas.
- Add a Codex pet section to the site with every animation and look direction. The hero portrait now acts out each cue with the Peon's animations, and the install section offers Sounds, Pet, or Both.
- Add animated pet previews to the README, a captioned `pet-preview.mp4`, and Peon-based banner, social card, and touch icon.
- Verify installation and diagnostics against the real artwork while preserving missing-art and conflict coverage.

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

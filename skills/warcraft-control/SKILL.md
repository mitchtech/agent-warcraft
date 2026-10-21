---
name: warcraft-control
disable-model-invocation: false
description: >-
  Inspect and control Agent Warcraft peon sound notifications without changing pet selection.
  TRIGGER when: the user says "mute the peon", "unmute the peon", "peon status",
  "Agent Warcraft status", "switch to Alliance", "switch to Horde", "Horde mode",
  "Alliance mode", "use both factions", "use the peasant", "stop the work work",
  "zug zug off", "turn off prompt sounds", "turn off job's done", "turn off work complete",
  "enable approval sounds", "peon attention mode", "turn off easter eggs",
  "stop the annoyed lines", "stop me busy leave me alone", "enable subagent sounds",
  "enable tool failure sounds", "enable compaction sounds", "turn on session end sounds",
  "gold alarm", "out of gold sound", "set a gold budget", "statusline gold meter",
  "preview a peon sound", "play we need more gold", or asks to inspect or adjust
  Agent Warcraft notifications.
  DO NOT TRIGGER when: the user wants operating system volume controls, unrelated
  notification settings, Agent Navi controls (use navi-control), Agent Johnny 5
  controls (use johnny5-control), pet artwork, or pet selection through the host picker.
---

# Agent Warcraft sound controls

Resolve this installed SKILL.md's directory. The bundled CLI is
`../../scripts/warcraft.mjs` relative to it. Run it with Node and a quoted absolute
path, rather than assuming a global `agent-warcraft` executable is installed.

- Inspect: `status`, `status --json`, `list`, or `config --effective`.
- Mute/unmute: `mute EVENT|easter-egg|all` or `unmute EVENT|easter-egg|all`.
- Faction: `faction horde`, `faction alliance`, or `faction both`.
- Presets: `preset attention` or `preset default`.
- Requested sound preview: `preview CLIP`.

Use `list` to resolve supported event and clip names. Translate a clear request
into the corresponding event:

| Request | Event |
|---|---|
| Prompt sounds ("work work", "I can do that") | `prompt_submitted` |
| Annoyed lines on rapid prompts ("Me busy, leave me alone!") | `annoyed` |
| Approval sounds, including the destructive-command alarm | `approval_required` |
| Questions | `input_required` |
| Idle or ready notices ("Something need doing?") | `ready_for_input` |
| "Work complete" / "Job's done" | `turn_completed` |
| Rate limit, billing, or budget exhausted ("We need more gold!") | `out_of_gold` |
| Status-line low-gold warning | `gold_low` |
| Output token limit ("We need more lumber") | `out_of_lumber` |
| Other API errors | `error` |
| Failed tool calls ("Can't build there") | `tool_failed` |
| Subagents starting ("Zug zug") | `subagent_started` |
| Compaction ("Inventory is full") | `context_compacting` |
| Session end | `session_ended` |
| Rare war cries ("For the Horde!", "For Lordaeron!") | `easter-egg` |

The Horde is the orc peon and advisor; the Alliance is the human peasant,
footman, and knight. "Use the peasant" means `faction alliance`. The destructive
alarm ("We're under attack!") is part of `approval_required`; it cannot be muted
separately without muting approvals. Ask only when the requested event is unclear.

The gold meter is a status-line command, not a hook. When asked to set it up or
to set a budget, explain the `gold.budgetUsd` and `gold.lowPercent` settings in
the config file and the `statusline` command documented in `docs/budget.md`, and
show the user the line to add. Do not edit the host's settings or status line yourself.

Change preferences only when the user requests that change. Inspection and
troubleshooting do not imply muting, unmuting, switching factions, applying a
preset, or playing audio. Always specify an event or explicit `all`. Global
mute/unmute preserves event preferences. Presets change event enablement and
preserve clips, faction, and global mute.

Changes persist outside plugin caches and take effect on the next hook. Report
the resulting status. If `AGENT_WARCRAFT_MUTE` overrides the saved preference, explain
that the user must change it in the agent's launch environment. Do not modify
shell startup files or host configuration automatically.

Pet installation and selection are independent. These controls never change
pets, register hooks, or approve agent actions.

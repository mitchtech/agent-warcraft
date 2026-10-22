# From install to first cue

Agent Warcraft is free to try. Sounds require Node.js 22+ on the agent's PATH and
local audio: `afplay` on macOS, a supported Linux player, or Windows PowerShell
on Windows. Remote hooks play on the remote machine unless an audio bridge is
already configured.

## Claude Code

Run in a terminal:

```bash
claude plugin marketplace add mitchtech/agent-warcraft
claude plugin install warcraft@agent-warcraft
```

Restart Claude Code. A new session should greet you with "Ready to work." and
the end of each turn should play "Work complete!". In a disposable project,
request a harmless operation that requires approval under your existing
permission settings; it should play "What you want?" or "Yes?" or, for a file
edit, "Hmmm?". Do not weaken permissions to make the
demonstration work. Use the explicit preview below to check audio separately.

## Codex

```bash
codex plugin marketplace add mitchtech/agent-warcraft
codex plugin add warcraft@agent-warcraft
```

Review and trust the installed hooks in Codex's hook settings, then restart.
Repeat the harmless approval check under your normal permission settings.
Installing or enabling the plugin alone does not establish hook trust.

## Codex pets

The Peon and Peasant pets install separately and need no Node.js:

```bash
curl -LO https://github.com/mitchtech/agent-warcraft/releases/latest/download/agent-warcraft-pet.zip
unzip agent-warcraft-pet.zip -d ~/.codex/pets
curl -LO https://github.com/mitchtech/agent-warcraft/releases/latest/download/agent-warcraft-peasant-pet.zip
unzip agent-warcraft-peasant-pet.zip -d ~/.codex/pets
```

With the standalone command, `agent-warcraft pet install` and
`agent-warcraft pet install peasant` do the same. Refresh the Codex desktop pet
picker, or enter `/pets Peon` or `/pets Peasant` in a graphics-capable Codex
CLI terminal. Installing a pet never selects it and never changes sound
settings.

## Already using Agent Navi or Agent Johnny 5?

All three plugins answer the same events. Enable one per host. For example,
`claude plugin disable johnny5@agent-johnny5` for Claude Code, or
`enabled = false` under `[plugins."johnny5@agent-johnny5"]` in
`~/.codex/config.toml` for Codex.

## Diagnose and preview without a global install

The bundled control skill supports requests such as "check the peon's sound
status," "mute the peon," "switch to Alliance," "turn off easter eggs," and
"use the attention preset." For an explicit terminal preview, use the repository CLI:

```bash
git clone https://github.com/mitchtech/agent-warcraft.git
cd agent-warcraft
node scripts/warcraft.mjs doctor
node scripts/warcraft.mjs preview orc-work-complete
```

`doctor` does not play audio or change settings. `preview` explicitly plays a
clip even when muted; it is an audio check, not proof that a host hook fired.
These commands need no npm install. To hear the destructive-command path without
an agent:

```bash
node scripts/warcraft.mjs play approval_required --tool Bash --command "rm -rf build"
```

That passes the string to the matcher only; nothing is executed. The usage
alarms can be heard the same way:

```bash
node scripts/warcraft.mjs play out_of_gold
node scripts/warcraft.mjs faction alliance
node scripts/warcraft.mjs play out_of_gold
node scripts/warcraft.mjs faction horde
```

To keep only attention-related events:

```bash
node scripts/warcraft.mjs preset attention
node scripts/warcraft.mjs status
```

The attention preset turns off session, prompt, annoyed, completion, error,
tool-failure, subagent, compaction, and session-end cues. Approval, question,
ready, and usage-alarm events remain enabled where the host exposes them.

```bash
node scripts/warcraft.mjs mute all
node scripts/warcraft.mjs unmute all
node scripts/warcraft.mjs preset default
```

Mute/unmute preserves individual event preferences. The default preset restores
event enablement and preserves global mute, faction, and custom clip choices.

## Remove sounds

Use the command for the host you installed:

```bash
claude plugin uninstall warcraft@agent-warcraft
```

```bash
codex plugin remove warcraft@agent-warcraft
```

Restart the host. Persistent sound settings are stored separately from plugin
caches.

If a check fails, report the host/version, operating system, expected event,
and redacted diagnostic error through [GitHub Issues](https://github.com/mitchtech/agent-warcraft/issues).
Do not include prompts, transcripts, credentials, or private configuration.

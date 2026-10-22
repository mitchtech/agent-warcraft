# Response sheet

Use these as factual starting points. Answer the person's question directly
and link only the relevant documentation.

**What is Agent Warcraft?** A free sound-notification plugin for coding agents
that plays *Warcraft III* voice lines. Native sounds support Claude Code, Codex,
and Gemini CLI; other tools can call the shared event interface. It is a
sibling of Agent Navi and Agent Johnny 5 and shares their runtime design.

**How is it different from peon-ping?** peon-ping is a much larger project with
hundreds of community sound packs across many games and IDEs, and it is a good
choice if you want that range. Agent Warcraft is one pack done in depth: usage
alarms from Claude Code's `StopFailure` error types, a status-line gold meter,
a destructive-command alarm, Horde and Alliance factions, and a zero-dependency
Node runtime shared with its siblings. Do not disparage peon-ping.

**Is it constantly talking?** Session, prompt, completion, and attention events
are enabled by default where supported. Use the attention preset to keep only
approvals, questions, ready notices, and usage alarms; mute individual events;
or mute everything. Error, tool-failure, subagent, compaction, and session-end
cues are off by default.

**Why does it say "Me busy, leave me alone"?** You sent three prompts within ten
seconds, like clicking a WC3 peon over and over. `agent-warcraft mute annoyed`
turns that off. Only timestamps are stored, never prompt text.

**When does it say "We need more gold"?** When Claude Code stops a turn with a
`rate_limit`, `billing_error`, or `account_on_hold` error, or when a usage-limit
wait ends without resuming. With the optional status-line meter it also warns
at 80% of your tightest limit and plays the gold line at 100%. Codex and Gemini
do not report API failures to hooks. See [budget](../budget.md).

**Does the gold meter know my real bill?** No. It reads the percentages Claude
Code sends to the status line and, if you set a budget, Claude Code's own
client-side cost estimate. It stores one level per session.

**Why "Job's done"? I thought peons said "Work complete".** They do. "Job's
done!" is the human peasant. `agent-warcraft faction alliance` switches to the
Alliance, and `faction both` mixes them.

**What is the "under attack" alarm?** When an approval's command matches a short
list of destructive patterns (recursive force deletes, force pushes, hard
resets, `git clean -f`, dropped or truncated tables, `mkfs`, `dd of=`,
`chmod -R 777`, and PowerShell recursive force removal), the approval plays
"We're under attack!" or "Our town is under attack!" instead of the ordinary cue.

**Is the alarm a safety feature?** No. It is a louder sound. It never blocks or
approves anything, and an indirect or obfuscated command gets the ordinary cue.
Keep your normal permission settings.

**Does it read my commands?** Only to set a yes/no flag inside the short-lived
hook process. The command is never passed to the playback worker, logged, or
stored. Local playback state stores hashed identifiers with timestamps or gold
levels only.

**What are the easter eggs?** About 2% of session, prompt, ready, and completion
cues are replaced by a war cry ("For the Horde!", "My life for the Horde!",
"For Lordaeron!"). They never replace approval, question, error, or alarm cues.
`agent-warcraft mute easter-egg` turns them off.

**Does it send telemetry?** No. It runs locally without runtime telemetry, and
the site loads no analytics. GitHub and social platforms keep their own aggregate
metrics.

**Why do I hear nothing?** Check Node.js on the hook process's PATH, restart the
agent, verify the local audio player/device, and inspect the mute state. Codex
also requires hook trust review. Use `doctor` for diagnostics and
`preview orc-ready` for an explicit audio check.

**I hear a fairy, a robot, and a peon.** Agent Navi or Agent Johnny 5 is
installed too. Enable one per host; see the
[install walkthrough](install.md#already-using-agent-navi-or-agent-johnny-5).

**Will it play on my laptop from SSH, WSL, or a container?** Not automatically.
Audio plays where the hook runs. A working audio bridge must already exist if
the execution environment and speakers are on different machines.

**Do all hosts expose the same events?** No. Claude has question, idle, usage,
tool-failure, and error mappings that Codex and Gemini lack. Completion is not
a task success detector. See [compatibility](../compatibility.md).

**Is there a Codex pet?** Two. The Peon (since v0.2.0) and the human Peasant
(since v0.3.0) each have nine animations and sixteen look directions. Install
from the release ZIPs without Node.js, or with `agent-warcraft pet install` and
`agent-warcraft pet install peasant`; they install side by side. Nine-row
atlases cover web pet uploads. See the [Peon](../pets.md) and
[Peasant](../peasant.md) guides.

**Does the pet follow my faction?** No. The faction picks whose voice you hear;
the pet is whichever one you choose in the Codex picker. Any combination works.

**Does the pet react to the sounds?** No. Codex animates the pet from its own
activity, and the sound plugin plays clips from hook events. They line up
because they watch the same agent, not because they talk to each other. The
site and pet video pair them on purpose to show both.

**Is the pet art from the game?** No. It was made with Codex image generation,
and no sprites, portraits, or models were extracted from Blizzard games. The
contributor's rights are licensed CC BY 4.0; Warcraft, the peon, and the peasant remain
Blizzard's.

**Is this official Blizzard software?** No. Warcraft and its voice lines belong
to Blizzard Entertainment. Code and configuration use MIT; the bundled audio is
excluded, and its provenance notice is not permission from the rights holder.
See the [audio notice](../../audio/NOTICE.md). If Blizzard asks, the clips come out.

**Can I use my own audio?** Yes. Configure your own audio directory with a
`<clip>.wav` for every name in `agent-warcraft list`, using 16-bit PCM WAV for
player compatibility. See [configuration](../../README.md#configuration).

**Was every platform physically tested?** CI exercises Node 22/24 on macOS,
Linux, and Windows with simulated players. Package tests exercise installed
bundles. Neither proves physical speaker output on every surface. Current
campaign checks are recorded in [validation](validation.md).

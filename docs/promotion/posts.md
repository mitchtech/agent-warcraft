# Public post drafts

Owner review required before publishing. These drafts describe documented
behavior, not fabricated user results. Attach the matching captioned preview
from [demos.md](demos.md). Keep its preview label visible. Substitute a live clip
only after the native capture checklist passes. Recheck community rules and
flair on publication day. Use one primary destination per post.

## R1 - r/ClaudeCode weekly showcase

I built Agent Warcraft, a free sound-notification plugin for Claude Code. It
plays *Warcraft III* peon lines on agent events: "Ready to work." when a
session starts, "What you want?" for an approval, "Work complete!" when a turn
finishes. When Claude Code stops on a rate limit or billing error, the orc
advisor tells you what every RTS player already knows: "We need more gold!"

The attached clip is an illustrated sound preview, not a live hook recording.

Install from your terminal:

```bash
claude plugin marketplace add mitchtech/agent-warcraft
claude plugin install warcraft@agent-warcraft
```

It needs Node.js 22+ and local audio. Restart Claude Code after installation.
It runs locally with no runtime telemetry, and the hooks never approve or block
actions. Approvals for `rm -rf` or a force push get "We're under attack!"
instead; that is a louder cue, not a safety check. Send three prompts in ten
seconds and the peon gets annoyed, exactly like clicking him too often.

There is an optional status-line gold meter that warns once when your 5-hour
or weekly limit runs low. Prefer the Alliance? `agent-warcraft faction alliance`
gets you "Job's done!" and "More gold is required."

Install details: https://github.com/mitchtech/agent-warcraft#install

Which cue would you turn off first? I am curious whether "Work complete" on
every turn is satisfying or too much.

## R2 - r/codex showcase

Title: I built Agent Warcraft: WC3 peon sound cues for Codex

I made Agent Warcraft, a free plugin that plays *Warcraft III* peon lines in
local Codex sessions. Session start gets "Ready to work.", prompts get "Work,
work.", approvals get "What you want?", and a finished turn gets "Work
complete!" Approvals whose command matches a short destructive list (`rm -rf`,
`git push --force`, `git reset --hard`, `DROP TABLE`, and similar) get "We're
under attack!" Only a yes/no flag leaves the hook; the command is never logged
or stored. Subagents can say "Zug zug." if you turn that cue on.

The attached video illustrates the sound; it is not a live Codex recording.

```bash
codex plugin marketplace add mitchtech/agent-warcraft
codex plugin add warcraft@agent-warcraft
```

Requirements: Node.js 22+, a local audio player/device, and a restart. Review
and trust the installed commands in Codex's hook settings. Installation alone
does not trust hooks.

There are no npm runtime dependencies or runtime telemetry. Hooks return
promptly and do not supply approval decisions. The rate-limit gold alarm is
Claude Code only, because Codex does not report API failures to hooks.
SSH/container execution plays where the hook runs, not automatically on your
laptop.

Install and compatibility details:
https://github.com/mitchtech/agent-warcraft#install

Where does setup get confusing: adding the marketplace, hook trust, or local
audio? If something fails, the host version and operating system would help me
reproduce it. Please leave private prompts and credentials out of reports.

## X1 - sound introduction

I built Agent Warcraft: WC3 peon sound cues for Claude Code, Codex, and Gemini CLI.

Turn finished: "Work complete!"
Rate limit hit: "We need more gold!"

Local. No telemetry. Free. Clip: illustrated preview.

https://github.com/mitchtech/agent-warcraft#install

## X2 - usage alarms

Claude Code tells hooks why a turn failed. Agent Warcraft listens.

rate_limit, billing_error: "We need more gold!"
max_output_tokens: "We need more lumber."
Status-line meter at 80%: "Our gold mine is running low."

https://github.com/mitchtech/agent-warcraft#gold-meter-and-usage-alarms

## X3 - the annoyed peon

Send your coding agent three prompts in ten seconds and the peon reacts the
way he did in 2002: "Me busy. Leave me alone!"

Prefer the Alliance? agent-warcraft faction alliance. "Help! Help! I'm being repressed!"

Clip: preview.

https://github.com/mitchtech/agent-warcraft#factions

## X4 - useful follow-up

Trying Agent Warcraft? Add the marketplace, install the plugin, then restart.

Codex also requires hook trust review. Remote sessions play audio on the
machine running the hook. Already running Agent Navi, Johnny 5, or Rocky? Enable one per host.

https://github.com/mitchtech/agent-warcraft#install

## X5 - meet the Peon

Agent Warcraft now ships a native Codex pet: the Peon.

Nine animations, sixteen look directions. Codex animates him; he works while
your agent works. No Node needed to install, just a ZIP.

Clip: atlas preview with bundled clips.

https://github.com/mitchtech/agent-warcraft#codex-pets

## X6 - meet the Peasant

The Alliance has a pet now too: Agent Warcraft adds the human Peasant as a
second native Codex pet.

Same nine animations and sixteen look directions as the Peon. Install one,
both, or neither:

agent-warcraft pet install peasant

Clip: atlas preview with bundled clips.

https://mitchtech.github.io/agent-warcraft/#pet

## R3 - r/codex pet showcase

Title: I made WC3 Peon and Peasant custom pets for Codex

I made two native custom pets for Codex: a Warcraft III-style orc Peon and his
Alliance counterpart, the human Peasant. Each has nine animations (idle,
working, waiting, review, blocked, moving, waving, jumping) and sixteen look
directions. The art was made with Codex image generation and
is CC BY 4.0; nothing was extracted from the game.

Install without Node.js:

```bash
curl -LO https://github.com/mitchtech/agent-warcraft/releases/latest/download/agent-warcraft-pet.zip
unzip agent-warcraft-pet.zip -d ~/.codex/pets
curl -LO https://github.com/mitchtech/agent-warcraft/releases/latest/download/agent-warcraft-peasant-pet.zip
unzip agent-warcraft-peasant-pet.zip -d ~/.codex/pets
```

Then refresh the desktop pet picker or enter `/pets Peon` or `/pets Peasant` in
a graphics-capable Codex CLI terminal. There are also nine-row atlases for web
pet uploads. The
attached video is an atlas preview, not a native recording.

The pets are independent of the project's sound plugin, which plays peon or
peasant lines on agent events. Install any combination.

Every animation is on the site: https://mitchtech.github.io/agent-warcraft/#pet

Horde or Alliance? And which state do you see most: working, waiting, or blocked?

## L1 - LinkedIn maker introduction

I built Agent Warcraft, a small sound-notification plugin for Claude Code,
Codex, and Gemini CLI. It plays *Warcraft III* peon lines when a coding agent
needs attention or finishes work, and the orc advisor's "We need more gold!"
when Claude Code stops on a rate limit or billing error.

The attached video is an illustrated preview of the cues, rather than a live
agent recording. The project is free to try.

The engineering problem was making a notification useful without making it
part of the agent's control flow. The hooks return promptly, leave approval
decisions alone, and tolerate missing audio or malformed input. The runtime
requires Node.js 22+ and has no npm dependencies or telemetry.

Code and installation:
https://github.com/mitchtech/agent-warcraft#install

If you use local coding agents, which event deserves a sound: approval, a
finished turn, or running out of usage?

## L2 - LinkedIn engineering follow-up

The most useful feature in Agent Warcraft started as a joke: playing "We need
more gold!" when a coding agent runs out of usage.

It turned into a small design exercise. Claude Code's `StopFailure` hook names
the error type, so a rate limit, a billing error, and an account hold can each
be told apart from a server error. Those three play the gold line;
`max_output_tokens` plays "We need more lumber."; everything else keeps an
optional generic cue.

A failed turn is too late, though. The optional status-line meter reads the
5-hour, weekly, and spend-limit percentages Claude Code already sends to the
status line and warns once per session when the tightest one crosses 80%. It
stores one number per session under a hashed name, and it always prints
something, because a status line that crashes is worse than none.

The same restraint applies everywhere else. The destructive-command alarm
reduces a command to a single boolean inside the hook process, and the
"annoyed peon" cue stores three timestamps, never prompt text.

The implementation and its tests are public:
https://github.com/mitchtech/agent-warcraft

## Replies and follow-up

Successful install: "Zug zug. Which host and OS are you using, and which cues
did you leave on?"

Continued use, after at least a week and only in a willing conversation:
"Have you kept the peon enabled? If you muted or removed it, what led to that?"

Install problem: "Which host/version and OS are you using? Please share the
error with private paths and credentials removed. The diagnostics and hook
trust notes are in the README."

Alarm as safety: "It is only a louder sound. It never blocks anything, and an
indirect or obfuscated command gets the ordinary cue. Keep your normal
permission settings."

When someone has found it useful: "A GitHub star helps other people find it if
you'd like to support the project." Do not ask for Reddit votes or coordinated
engagement.

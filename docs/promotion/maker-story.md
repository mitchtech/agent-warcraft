# Why I built Agent Warcraft

Coding agents spend part of their time waiting for a person, and part of it
finishing work you are not watching. I had already built Agent Navi and Agent
Johnny 5 to give those moments a familiar sound. Agent Warcraft gives them the
most familiar one I know: a *Warcraft III* peon.

Anyone who played in 2002 already knows the vocabulary. "Ready to work." when a
unit is trained. "Work, work." when you give it an order. "Work complete!" when
the building is done. Those map onto a coding agent almost without translation:
a session starts, you send a prompt, a turn finishes.

The new idea came from the advisor. "We need more gold!" is what the game says
when you try to spend money you do not have. Coding agents have exactly that
failure: a rate limit, a billing error, a usage window that ran out mid-task.
Claude Code's `StopFailure` hook names the error type, so those three can be
told apart from a server error and get the gold line. Hitting the output token
limit gets "We need more lumber."

A failed turn is late notice, so there is also an optional status-line meter.
Claude Code already sends the status line its 5-hour, weekly, and spend-limit
percentages; the meter shows what is left of the tightest one and plays "Our
gold mine is running low." once per session when it crosses a threshold. It
stores one number per session, and it always prints a line, because a status
line that fails is worse than none.

The peon also has a temper. In the game, clicking a unit over and over gets
progressively less patient replies. Here, the third prompt inside ten seconds
gets "Me busy. Leave me alone!" instead of "Work, work." The hook keeps three
timestamps to decide that, never the prompt text.

Some people grew up on the other side, so there is a faction setting. The
Alliance swaps in the human peasant, footman, and knight: "Job's done!", "More
gold is required.", and a peasant who, when annoyed, quotes Monty Python. Every
default cue has a line for both factions, so switching never silences an event.

The rest of the design is inherited from its siblings. Host hooks return
promptly and fail open on malformed input, missing audio, invalid configuration,
and playback failure. They never approve or block actions. Approvals for `rm
-rf` or a force push play "We're under attack!", a cue and not a safety check;
the command is reduced to a yes/no flag inside the hook and never stored. The
shared player uses Node.js 22+ with no npm runtime dependencies across macOS,
Linux, and Windows.

The audio got the same treatment as Johnny 5's. A build script records each
source URL and hash, the archive member where one applies, and the output hash,
and matches loudness across all 58 clips. I transcribed every result to confirm
the words survived the trim. Speech-to-text heard "Something need doing?" as
"Something you're doing?", which says more about orc grammar than the trim.

The project now has a face, too. The Peon is a native Codex pet with nine
animations and sixteen look directions, made with Codex's own image generation
rather than lifted from the game. Codex animates him from its activity, so he
swings his pickaxe while the agent works and holds his head when something
fails. He installs from a ZIP without Node.js, and he is independent of the
sounds; plenty of people will want one without the other. The Alliance got its
own pet next: a bearded human Peasant in a blue hood, with the same full set of
animations, installed beside the Peon or instead of him.

The project separates its licenses: MIT for code and configuration, CC BY 4.0
for the pet artwork, and a separate notice for the *Warcraft III* recordings, which belong to Blizzard
Entertainment. There is no claim of official affiliation or ownership of the
characters or the audio.

If you try it, I would like to know which cues you keep, and whether "Work
complete" after every turn is satisfying or too much. Those answers are more
useful than another feature imagined in advance of someone needing it.

[Install Agent Warcraft](https://github.com/mitchtech/agent-warcraft#install)
or [hear every clip](https://mitchtech.github.io/agent-warcraft/).

# Sound notes

Why each event plays what it plays, how the faction modes divide the lines, and
how to change them.

## Mapping

Each row lists the Horde clips, then the Alliance clips.

| Event | Horde / Alliance clips | Why |
|---|---|---|
| `session_started` | `orc-ready` / `human-ready` | "Ready to work." is the line a worker says when it is trained. |
| `prompt_submitted` | `orc-i-can-do-that`, `orc-be-happy-to`, `orc-work-work`, `orc-okie-dokie` / `human-righto`, `human-yes-me-lord`, `human-alright`, `human-off-i-go` | The acknowledgments a worker gives when you hand it an order. |
| `annoyed` | `orc-whaaat`, `orc-me-busy`, `orc-no-time-for-play`, `orc-not-that-kind-of-orc` / `human-didnt-vote`, `human-witch`, `human-repressed`, `human-horse-kicked` | The lines Warcraft III saves for clicking the same unit over and over, which is what three prompts in ten seconds looks like. |
| `approval_required` | `orc-what-you-want`, `orc-yes` / `human-yes-milord` | Selection lines: the unit is waiting for your decision. |
| Approval for shell or edit | `orc-hmm` / `human-what` | A shorter, wary query for a tool about to touch your files. |
| Approval for a destructive command | `orc-under-attack`, `orc-town-under-attack` / `human-forces-under-attack`, `human-town-under-siege` | The advisor's attack warnings, the most urgent lines in the game. |
| `input_required` | `orc-hmm` / `human-what` | The agent is asking you directly. |
| `ready_for_input` | `orc-something-need-doing` / `human-more-work` | An idle worker asking for its next job. |
| `turn_completed` | `orc-work-complete` / `human-jobs-done` | The lines people install this for. On by default, unlike the siblings. |
| `out_of_gold` | `orc-need-more-gold` / `human-more-gold` | Usage limit or budget spent: the treasury is empty. |
| `gold_low` | `orc-gold-mine-low` / `human-gold-mine-low` | The gold meter's early warning. |
| `out_of_lumber` | `orc-need-more-lumber` / `human-more-lumber` | The reply ran past the output token limit, the second resource. |
| `out_of_food` | `orc-build-more-burrows` / `human-build-more-farms` | The context window is nearly full, as when food reaches its cap and nothing more can be trained. |
| `error` | `orc-hero-slain` / `human-hero-fallen` | A turn died on an API error. Off by default. |
| `tool_failed` | `orc-cant-build-there` / `human-cant-build-there` | The order was valid but the ground was not. Off by default; tool failures are frequent. |
| `subagent_started` | `orc-zug-zug`, `orc-dabu`, `orc-loktar` / `human-aye-my-lord`, `human-on-my-way`, `human-of-course` | Grunt and footman acknowledgments: another unit sets off. Off by default. |
| `context_compacting` | `orc-inventory-full` / `human-inventory-full` | The hero's pack is full; compaction makes room. Off by default. |
| `session_ended` | `orc-death` / `human-groan` | The worker's last sound. Off by default. |
| Easter egg | `orc-for-the-horde`, `orc-my-life-for-the-horde`, `orc-why-not` / `human-for-lordaeron`, `human-ready-for-action` | Rare war cries, only on non-urgent cues. |

Every clip, its words, and its source are listed in the [audio notice](../audio/NOTICE.md).

## Faction modes

| `faction` | What plays |
|---|---|
| `horde` (default) | Only the Horde clips in each list. |
| `alliance` | Only the Alliance clips. |
| `both` | Any clip in the list. |
| `random` | One faction per session, chosen from a hash of the session ID, so a session keeps the same voice from start to finish. |
| `duo` | One faction per event, as below. |

In duo mode the Peon handles the work chatter and the Alliance reports results
and raises the alarms:

| Horde | Alliance |
|---|---|
| `session_started`, `prompt_submitted`, `annoyed`, `subagent_started`, `tool_failed`, `session_ended` | `approval_required`, `input_required`, `ready_for_input`, `turn_completed`, `out_of_gold`, `gold_low`, `out_of_lumber`, `out_of_food`, `error`, `context_compacting` |

So a turn starts with "Work, work." and ends with "Job's done!". Easter eggs
follow the event they replace.

A custom clip list with no clips from the chosen faction plays as written, so
no mode can silence an event.

## Alternatives worth trying

Lines that fit other events well:

- `orc-zug-zug` or `human-of-course` on `prompt_submitted`, for a shorter
  acknowledgment.
- `orc-yes` on `ready_for_input`.
- `orc-why-not` on `turn_completed`, for a peon who is less sure of the result.
- `orc-hero-slain` on `tool_failed`, for more drama than the failure deserves.

Set them in `~/.config/agent-warcraft/config.json` (`%APPDATA%` on Windows).
Each list picks one clip at random after the faction filter:

```json
{
  "events": {
    "prompt_submitted": { "clips": ["orc-zug-zug", "orc-work-work", "human-of-course"] },
    "ready_for_input": { "clips": ["orc-yes", "human-more-work"] }
  }
}
```

`agent-warcraft list` prints every clip name, and `agent-warcraft preview CLIP`
plays one without changing anything.

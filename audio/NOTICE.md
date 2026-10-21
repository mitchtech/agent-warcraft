# Audio provenance and rights

The WAV files in this directory are derived from *Warcraft III: Reign of Chaos*
(2002, Blizzard Entertainment). Blizzard Entertainment retains all rights to the
game audio, including every voice line here. Warcraft is a trademark of
Blizzard Entertainment. No ownership of these clips is claimed, and no
affiliation with or endorsement by Blizzard is implied.

The repository's MIT license covers source code and configuration only. It
does not cover these recordings or grant any rights to the game's audio.

The clips are included for personal, non-commercial use. This notice records
their provenance; it is not a license from the rights holder. They will be
removed on request from Blizzard Entertainment.

## Sources and processing

[`sources.json`](sources.json) lists every source URL, its SHA-256, the archive
member where one applies, and the hash of each committed output. The sources are
community archives of the original game files: the warcraft.wiki.gg file pages
and The Sounds Resource's *Warcraft III* "Interface" and "Orc (English)"
archives. Neither publishes a license for the recordings. Every clip's words
were checked against a speech-to-text transcript before it was committed.

The Sounds Resource sits behind a browser challenge, so rebuilding those clips
needs the two archives downloaded once in a browser and saved in the build
cache under their SHA-256 (`--cache DIR`; the error message names the file).

[`scripts/build-audio.py`](../scripts/build-audio.py) trims leading and trailing
room tone, applies one linear gain to reach -16 LUFS integrated with a peak
limiter, adds 10-20 ms fades, and writes 16-bit mono PCM WAV at 32 kHz.
`--check` verifies the committed files without downloading anything.

| File | Faction | Line | Length | Source |
|---|---|---|---|---|
| `orc-ready.wav` | Horde | Ready to work. | 0.84 s | warcraft.wiki.gg (`PeonReady1.wav`) |
| `orc-something-need-doing.wav` | Horde | Something need doing? | 1.13 s | warcraft.wiki.gg (`PeonWhat4.wav`) |
| `orc-yes.wav` | Horde | Yes? | 0.56 s | warcraft.wiki.gg (`PeonWhat1.wav`) |
| `orc-hmm.wav` | Horde | Hmmm? | 0.43 s | warcraft.wiki.gg (`PeonWhat2.wav`) |
| `orc-what-you-want.wav` | Horde | What you want? | 0.78 s | warcraft.wiki.gg (`PeonWhat3.wav`) |
| `orc-i-can-do-that.wav` | Horde | I can do that. | 0.65 s | warcraft.wiki.gg (`PeonYes1.wav`) |
| `orc-be-happy-to.wav` | Horde | Be happy to. | 0.86 s | warcraft.wiki.gg (`PeonYes2.wav`) |
| `orc-work-work.wav` | Horde | Work, work. | 0.86 s | warcraft.wiki.gg (`PeonYes3.wav`) |
| `orc-okie-dokie.wav` | Horde | Okey dokey. | 1.01 s | warcraft.wiki.gg (`PeonYes4.wav`) |
| `orc-whaaat.wav` | Horde | Whaaat? | 0.90 s | warcraft.wiki.gg (`PeonPissed1.wav`) |
| `orc-me-busy.wav` | Horde | Me busy. Leave me alone! | 1.98 s | warcraft.wiki.gg (`PeonPissed2.wav`) |
| `orc-no-time-for-play.wav` | Horde | No time for play. | 1.14 s | warcraft.wiki.gg (`PeonPissed3.wav`) |
| `orc-not-that-kind-of-orc.wav` | Horde | Me not that kind of orc! | 1.69 s | warcraft.wiki.gg (`PeonPissed4.wav`) |
| `orc-work-complete.wav` | Horde | Work complete! | 0.88 s | warcraft.wiki.gg (`PeonJobDone.wav`) |
| `orc-need-more-gold.wav` | Horde | We need more gold! | 1.37 s | The Sounds Resource (`GruntNoGold1.wav`) |
| `orc-need-more-lumber.wav` | Horde | We need more lumber. | 1.47 s | The Sounds Resource (`GruntNoLumber1.wav`) |
| `orc-gold-mine-low.wav` | Horde | Our gold mine is running low. | 1.56 s | The Sounds Resource (`GruntGoldMineLow1.wav`) |
| `orc-under-attack.wav` | Horde | We're under attack! | 1.34 s | The Sounds Resource (`GruntUnitAttack1.wav`) |
| `orc-town-under-attack.wav` | Horde | Our town is under attack! | 1.82 s | The Sounds Resource (`GruntTownAttack1.wav`) |
| `orc-inventory-full.wav` | Horde | Inventory is full. | 1.41 s | The Sounds Resource (`GruntInventoryFull1.wav`) |
| `orc-hero-slain.wav` | Horde | Our hero has been slain! | 1.83 s | The Sounds Resource (`GruntHeroDies1.wav`) |
| `orc-cant-build-there.wav` | Horde | Can't build there. | 1.07 s | The Sounds Resource (`PeonCannotBuildThere1.wav`) |
| `orc-zug-zug.wav` | Horde | Zug zug. | 0.51 s | warcraft.wiki.gg (`GruntYes4.wav`) |
| `orc-dabu.wav` | Horde | Dabu. | 0.48 s | warcraft.wiki.gg (`GruntYes1.wav`) |
| `orc-loktar.wav` | Horde | Lok'tar. | 0.73 s | warcraft.wiki.gg (`GruntYes2.wav`) |
| `orc-death.wav` | Horde | (peon death) | 1.49 s | The Sounds Resource (`PeonDeath.wav`) |
| `orc-for-the-horde.wav` | Horde | For the Horde! | 1.53 s | warcraft.wiki.gg (`GruntWarcry1.wav`) |
| `orc-my-life-for-the-horde.wav` | Horde | My life for the Horde! | 1.69 s | warcraft.wiki.gg (`GruntReady1.wav`) |
| `orc-why-not.wav` | Horde | Why not? | 0.63 s | warcraft.wiki.gg (`PeonWarcry1.wav`) |
| `human-ready.wav` | Alliance | Ready to work. | 1.05 s | warcraft.wiki.gg (`PeasantReady1.wav`) |
| `human-yes-milord.wav` | Alliance | Yes, milord? | 0.96 s | warcraft.wiki.gg (`PeasantWhat1.wav`) |
| `human-what.wav` | Alliance | What? | 0.26 s | warcraft.wiki.gg (`PeasantWhat4.wav`) |
| `human-more-work.wav` | Alliance | More work? | 0.77 s | warcraft.wiki.gg (`PeasantWhat3.wav`) |
| `human-righto.wav` | Alliance | Right-o. | 0.76 s | warcraft.wiki.gg (`PeasantYes1.wav`) |
| `human-yes-me-lord.wav` | Alliance | Yes, me lord. | 0.87 s | warcraft.wiki.gg (`PeasantYes2.wav`) |
| `human-alright.wav` | Alliance | All right. | 0.68 s | warcraft.wiki.gg (`PeasantYes3.wav`) |
| `human-off-i-go.wav` | Alliance | Off I go, then! | 0.99 s | warcraft.wiki.gg (`PeasantYes4.wav`) |
| `human-didnt-vote.wav` | Alliance | You're the king? Well, I didn't vote for you. | 3.34 s | warcraft.wiki.gg (`PeasantPissed1.wav`) |
| `human-witch.wav` | Alliance | We found a witch! May we burn her? | 2.58 s | warcraft.wiki.gg (`PeasantPissed2.wav`) |
| `human-repressed.wav` | Alliance | Help! Help! I'm being repressed! | 2.54 s | warcraft.wiki.gg (`PeasantPissed3.wav`) |
| `human-horse-kicked.wav` | Alliance | A horse kicked me once. It hurt. | 3.05 s | warcraft.wiki.gg (`PeasantPissed4.wav`) |
| `human-jobs-done.wav` | Alliance | Job's done! | 0.67 s | warcraft.wiki.gg (`PeasantBuildingComplete1.wav`) |
| `human-more-gold.wav` | Alliance | More gold is required. | 1.31 s | The Sounds Resource (`KnightNoGold1.wav`) |
| `human-more-lumber.wav` | Alliance | More lumber is required. | 1.59 s | The Sounds Resource (`KnightNoLumber1.wav`) |
| `human-gold-mine-low.wav` | Alliance | Our gold mine is running low. | 1.64 s | The Sounds Resource (`KnightGoldMineLow1.wav`) |
| `human-forces-under-attack.wav` | Alliance | Our forces are under attack! | 1.56 s | The Sounds Resource (`KnightUnitAttack1.wav`) |
| `human-town-under-siege.wav` | Alliance | Our town is under siege. | 1.91 s | The Sounds Resource (`KnightTownAttack1.wav`) |
| `human-inventory-full.wav` | Alliance | Inventory is full. | 1.28 s | The Sounds Resource (`KnightInventoryFull1.wav`) |
| `human-hero-fallen.wav` | Alliance | Our hero has fallen. | 1.32 s | The Sounds Resource (`KnightHeroDies1.wav`) |
| `human-cant-build-there.wav` | Alliance | I can't build there. | 0.86 s | The Sounds Resource (`PeasantCannotBuildThere1.wav`) |
| `human-aye-my-lord.wav` | Alliance | Aye, my lord. | 0.81 s | warcraft.wiki.gg (`FootmanYes1.wav`) |
| `human-on-my-way.wav` | Alliance | On my way. | 0.70 s | warcraft.wiki.gg (`FootmanYes2.wav`) |
| `human-of-course.wav` | Alliance | Of course. | 0.71 s | warcraft.wiki.gg (`FootmanYes4.wav`) |
| `human-for-lordaeron.wav` | Alliance | For Lordaeron! | 1.62 s | warcraft.wiki.gg (`FootmanWarcry1.wav`) |
| `human-ready-for-action.wav` | Alliance | Ready for action. | 0.87 s | warcraft.wiki.gg (`FootmanReady1.wav`) |
| `human-groan.wav` | Alliance | (weary peasant groan) | 0.90 s | warcraft.wiki.gg (`PeasantWarcry1.wav`) |

Use the user audio directory setting to supply your own replacement recordings
without editing installed plugin files.

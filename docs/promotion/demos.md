# Media and live capture scripts

## Available previews

These assets are illustrated previews assembled from the bundled WAV files and
the site's fonts. They do not show a native host, a real approval dialog, or
physical speaker playback. Keep their labels visible and describe them as previews.

| Asset | Duration | Use |
|---|---|---|
| [Sound preview](../../assets/promotion/sound-preview.mp4) | 27 seconds | Main sound posts; cues at 0.5 s (ready to work), 4.5 s (what you want), 8.5 s (our town is under attack, with a force push on screen), 13.5 s (work complete), 17.5 s (we need more gold) |
| [Faction preview](../../assets/promotion/faction-preview.mp4) | 15 seconds | Faction post; the Peasant waves, jumps, and slumps with Alliance cues at 0.5 s (ready to work), 5.5 s (job's done), 10.5 s (more gold is required) |
| [Pet preview](../../assets/promotion/pet-preview.mp4) | 33 seconds | Pet posts; the Peon idles, then works with "work, work" at 4.5 s, waits with "what you want" at 8.5 s, jumps with "work complete" at 12.5 s, slumps with "we need more gold" at 16.5 s; the Peasant idles at 20 s, jumps with "job's done" at 24.5 s, and waves over the install command |

The pet preview pairs atlas animations with matching clips to show both
components together. In real use Codex animates the pet from its own activity
and the plugin plays the sound; they do not signal each other. Keep its
caption visible.

Each MP4 is 1080 x 1080, 15 fps, H.264/yuv420p with AAC audio, burned-in
captions, and a fast-start header. A framed portrait on screen sweeps each
clip's waveform in sync with its audio. Matching `.srt` files and PNG posters live
beside the videos. The [manifest](../../assets/promotion/manifest.json) records
hashes, source files, tool versions, and limitations. The README's
[waveform GIFs](../../assets/previews/orc-work-complete.gif) remain available.

Build locally with existing Pillow and FFmpeg installations:

```bash
python3 docs/promotion/build-media.py
```

This script never installs tools, plays audio through speakers, uses account
credentials, or publishes files. Code is MIT. Video composition does not grant
rights to the *Warcraft III* audio, which belongs to Blizzard Entertainment.
Never add Blizzard logos, box art, or game footage. Preserve the [audio notice](../../audio/NOTICE.md)
and [font notice](../../site/fonts/OFL.md).

## Native approval recording - 20-30 seconds

Use this script when a verified host recording is available. Capture a fresh
disposable project and only the relevant host window. Keep your normal permission
settings. Capture application/system audio if supported; a screen recording
without an audio track does not establish an audible cue.

| Time | Capture | Caption |
|---|---|---|
| 0-3 s | Host and exact version visible; harmless task underway | Your agent is waiting for approval |
| 3-8 s | A real approval request and the corresponding cue | What you want? |
| 8-15 s | Your response to the dialog; retain enough context to understand it | You make the decision |
| 15-22 s | Verified install commands for that host | Agent Warcraft - local sound cues |
| 22-27 s | Repository address | github.com/mitchtech/agent-warcraft |

Use a request to write a temporary text file in the disposable project if it
requires approval under the existing policy. If it is already approved, do not
manufacture an approval dialog or substitute a `play` invocation while claiming
native behavior. Match the caption to the actual cue: file-edit requests play
"Hmmm?" rather than "What you want?".

## Destructive-command recording - 10-15 seconds

In a disposable directory containing only a throwaway `build/` folder, ask the
agent to delete it with `rm -rf build`. Record the approval dialog and the
"We're under attack!" or "Our town is under attack!" cue, then deny or approve
as you would normally.
Never point the demonstration at anything you would mind losing, and never
weaken permissions to stage it. Caption it as a cue, not a safeguard.

Pass criteria for both recordings: visible native dialog, matching audio track,
exact host/version noted in the capture record, readable captions at phone
width, no private content, and no dubbed cue presented as live playback. Replace
the preview disclaimer in the relevant post only after these criteria pass.

## Out-of-gold recording

Do not burn through a real usage limit to stage this. Record it only if a rate
limit happens during ordinary work, with the StopFailure message visible.
Otherwise use the sound preview, labeled as a preview, or show the status-line
meter with a low `gold.lowPercent` so the "running low" cue plays honestly.

## Native pet recording - 10-20 seconds

With the Peon or the Peasant installed and selected, record the Codex desktop pet (or a
graphics-capable Codex CLI terminal) through one ordinary task: idle, working,
then waiting or review as Codex reports them. Note the host and version. Do not
composite the atlas over a host window and present it as native rendering.

## Quiet configuration recording - 10-15 seconds

Show the current status; invoke `preset attention` through the bundled skill or
repository CLI; show the resulting enabled events. Caption session/prompt cues
as disabled and attention events as host-dependent. Do not claim a silent event
was observed merely because no audio was captured.

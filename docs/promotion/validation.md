# Promotion validation

Campaign publications have not started. No social accounts were modified, no
messages were sent, and no directory submissions were made. Local evidence under
`dist/promotion/` is ignored by Git.

## Initial observations

Capture the first metrics snapshot after the v0.1.0 release and before any
promotion:

```bash
python3 docs/promotion/capture-metrics.py
```

Record the star and fork counts, the release asset IDs with their initial
download counts, and the traffic window here. Treat downloads and clones from
release verification and isolated install checks as validation activity, not
campaign adoption.

| Measure | Initial value | Captured |
|---|---|---|
| Stars / forks | Pending | Pending |
| Traffic window views / unique visitors | Pending | Pending |
| Release assets and downloads | Pending | Pending |

## Pre-release checks

Completed on October 21, 2026 against the local build:

- `npm run check`, `npm test` (43 tests), and `npm run test:package` passed.
- `python3 scripts/build-audio.py --check` verified all 56 clips. Each source
  and each built clip was transcribed with whisper.cpp to confirm the intended
  line survived trimming, and every clip is normalized to -16 LUFS integrated.
- `python3 scripts/check-pet.py` reported the pet as not bundled, as intended.
- `python3 scripts/build-assets.py --check` matched committed preview pixels.
- A local build of the site was checked in Chromium at 1440 x 900 and 390 x 844,
  in both factions. There was no horizontal overflow, fonts loaded, and the
  console showed no errors after one hotkey fix. Three portrait clicks produced
  the annoyed line, an empty demo treasury produced the out-of-gold line, and a
  real `w` keypress played its command-card clip.
- The registered hook commands were run with real Claude and Codex payloads on
  macOS with `afplay`: session start, `StopFailure` rate_limit and
  max_output_tokens, a destructive approval, Codex Stop (stdout exactly `{}`),
  three rapid prompts (the third escalated to `annoyed`), and the status-line
  meter crossing 80% (one `gold_low`, no repeat at 85%).
- Both promotional MP4s were rendered: 27 and 15 seconds, 1080 x 1080 H.264
  with AAC audio.

Known behavior: `afplay` holds the audio device for roughly 0.9 seconds after a
clip ends, and the global lock spans the player's whole run. A second cue
arriving within about 2.5 seconds of the first is dropped, as in the sibling
projects.

## Remaining native checks

The following have not been verified by automated, package, or browser checks:

- Physical speaker output from an actual Claude Code approval request.
- The destructive-command cue from an actual Claude Code `rm -rf` approval.
- An actual Claude Code `StopFailure` from a real rate limit.
- Physical speaker output from an actual trusted Codex approval request.
- End-to-end native behavior on Linux or Windows.
- The published Pages site (only a local build has been checked).

The committed MP4s are labeled illustrated previews, not proof of those checks.
Before publishing a claim of native behavior personally observed, complete the
[capture script](demos.md) and record host/version, OS, event, and result here.

| Check | Host/version | OS | Event/result | Evidence |
|---|---|---|---|---|
| Claude physical approval cue | Pending | Pending | Pending | Pending |
| Claude destructive-command cue | Pending | Pending | Pending | Pending |
| Claude rate-limit gold cue | Pending | Pending | Pending | Pending |
| Codex trusted physical approval cue | Pending | Pending | Pending | Pending |

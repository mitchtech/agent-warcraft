# Peon pet

The sound plugin and the Codex pet are independent. The local v2 pet has nine
animations and sixteen clockwise look directions. The host controls its
animations without additional hooks or a daemon.

## Installation

From this source checkout:

```bash
node scripts/warcraft.mjs pet install
node scripts/warcraft.mjs doctor --pet
```

With a CLI package that includes the artwork, use `agent-warcraft pet install`
and `agent-warcraft doctor --pet`. Older packages without artwork continue to
report `not-bundled` without changing local pet files.

Pet-enabled [Releases](https://github.com/mitchtech/agent-warcraft/releases)
include `agent-warcraft-pet.zip` for manual installation. Extract the `peon`
directory under your configured Codex home's `pets` directory:

```text
~/.codex/pets/peon/
  pet.json
  spritesheet.webp
  LICENSE.txt
  NOTICE.md
```

If `CODEX_HOME` is configured, use `<CODEX_HOME>/pets/peon/` instead. Manual
installation needs no Node.js, Python, audio player, or sound plugin. Preserve
a backup before replacing a different existing pet.

## Selection and compatibility

After installation, refresh the compatible host's pet picker and choose
Peon. Installation never changes the selected pet or other host settings.
The local bundle targets Codex sprite version 2. Claude Code and Gemini use
this repository's sounds; no native pet integration for those hosts is
provided here. ChatGPT account pets are separate from the local bundle.
[Official pet documentation](https://learn.chatgpt.com/docs/pets)

## Installer behavior

The CLI copies the four bundle files and a local ownership
record into `$CODEX_HOME/pets/peon` (default `~/.codex/pets/peon`). It
leaves avatar selection, agent settings, hooks, and audio configuration
unchanged. An identical install is a no-op. A matching manual installation
remains unmanaged.

Different files require `agent-warcraft pet install --replace`. The previous entire
directory is renamed to `peon.backup-<unique-suffix>` next to the new
installation. Files and symbolic links at the target directory path are never
replaced.

Status reports `not-bundled`, `not-installed`, `matching`, `modified`, or
`conflict`. Uninstall removes only an unchanged CLI-owned installation, even
when the current package has no art. It refuses edited files, unknown additional
files, symbolic links, and unmanaged installations.

```bash
agent-warcraft pet status --json
agent-warcraft pet uninstall
```

## Artwork and validation

The active atlas lives in `pets/peon/spritesheet.webp`. The original PNG
is preserved byte-for-byte in `assets/original/peon`. Lossless WebP encoding
preserves every decoded RGBA pixel. Source and active hashes are recorded in
`assets/pet-revision.json` and the [artwork notice](../pets/peon/NOTICE.md).
The artwork license applies to the contributor's rights; third-party character
rights remain with their respective owners.

`python3 scripts/check-pet.py` validates the 1536 x 2288 RGBA WebP, all 73
occupied cells, the 15 transparent cells, and transparent-pixel RGB cleanup.
`python3 scripts/package-pet.py` builds a reproducible four-file pet ZIP;
release packaging includes it automatically.

The creation workflow reviewed all nine animation states and sixteen gaze
directions, including an independent blind direction check. Repository tests
exercise real-art installation and package diagnostics, with small fixtures
for conflicts and missing-art behavior. Native desktop and terminal rendering
have not been independently verified for this bundle.

# Human Peasant pet

<p align="center"><img src="../assets/previews/peasant-idle.gif" width="160" alt="Peasant idling"> <img src="../assets/previews/peasant-working.gif" width="160" alt="Peasant working"> <img src="../assets/previews/peasant-failure.gif" width="160" alt="Peasant blocked"></p>

The Warcraft III-era human Peasant is the Alliance counterpart to the orc
[Peon](pets.md). His local v2 bundle contains nine animation states and sixteen
clockwise look directions. Sounds and pet selection remain independent.

## Local installation

From a release containing the Peasant artwork:

```bash
curl -LO https://github.com/mitchtech/agent-warcraft/releases/latest/download/agent-warcraft-peasant-pet.zip
unzip agent-warcraft-peasant-pet.zip -d ~/.codex/pets
```

The ZIP contains exactly these four files:

```text
peasant/
  pet.json
  spritesheet.webp
  LICENSE.txt
  NOTICE.md
```

With the standalone command, or from a source checkout with
`node scripts/warcraft.mjs`:

```bash
agent-warcraft pet install peasant
agent-warcraft doctor --pet peasant
```

`pet status peasant` and `pet uninstall peasant` work the same way; without a
name, the pet commands target the Peon. The installer writes
`$CODEX_HOME/pets/peasant` (or `~/.codex/pets/peasant`), never selects the pet,
refuses to overwrite a different existing `peasant` directory unless you pass
`--replace`, and then keeps a backup. The Peon and the Peasant install side by
side. Refresh the host's pet picker and choose Peasant, or enter
`/pets Peasant` in a graphics-capable Codex CLI terminal.

The bundle targets compatible Codex desktop and graphics-capable CLI hosts.
ChatGPT account pets are separate from local bundles. Native host rendering
has not been independently verified for Peasant.

## Web upload

Use `agent-warcraft-peasant-pet-web.webp` from a release or
`assets/exports/agent-warcraft-peasant-pet-web.webp` in the checkout. This
1536 x 1872 transparent lossless WebP preserves the nine animation rows;
the local v2 sheet's two look-direction rows are omitted. Uploading it
creates a separate account pet. Retain the artwork credit and license.

## Assets and validation

- Active local atlas: `pets/peasant/spritesheet.webp` (1536 x 2288).
- Exact original PNG and local manifest: `assets/original/peasant`.
- Provenance and hashes: `assets/peasant-pet-revision.json`.
- Artwork credit and contributor rights: [NOTICE.md](../pets/peasant/NOTICE.md)
  and [CC BY 4.0 license](../pets/peasant/LICENSE.txt).

```bash
python3 scripts/check-pet.py --pet peasant
python3 scripts/export-pet-web.py --pet peasant
python3 scripts/package-pet.py --pet peasant
```

Running `check-pet.py` or `export-pet-web.py` without `--pet` processes both
Peon and Peasant. `package-release.py` includes both local ZIPs and both web
exports. `build-assets.py` derives the committed Peasant preview GIFs from
the active atlas, with `--check` for pixel comparison.

The creation workflow reviewed every animation and look direction, including
an independent blind axis check and an idle-to-jump-to-idle transition.
Repository validation checks all 73 occupied cells, 15 transparent cells,
transparent-pixel RGB cleanup, and exact web-export pixels. Package checks
verify the Peasant files in both npm and Gemini distributions and install,
diagnose, and remove the Peasant from each. Installer tests install the real
Peasant bundle beside the Peon.

# Peon pet artwork

This artwork depicts a Warcraft III-era orc peon. Michael J. Mitchell
requested it on October 21, 2026, and created it with Codex using built-in
image generation. A canonical character image grounded the animation strips
and look-direction strips. Deterministic processing extracted, registered,
assembled, cleaned, and validated the generated pixels. No sprites, portraits,
or models were extracted from Blizzard games.

Warcraft and the peon belong to Blizzard Entertainment. This project is not
affiliated with or endorsed by Blizzard. Game audio has a separate
[rights notice](../../audio/NOTICE.md).

The contributor's rights in this artwork are licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), as described in
[LICENSE.txt](LICENSE.txt). Suggested credit: "Peon pet artwork by Michael
J. Mitchell / mitchtech, CC BY 4.0, https://github.com/mitchtech/agent-warcraft."

## Format and validation

- ID: `peon`; display name: `Peon`; sprite version: `2`.
- Transparent RGBA WebP, 1536 x 2288 pixels, with 192 x 208 cells.
- Nine animation rows: idle, moving right, moving left, waving, jumping,
  failure, waiting, working, and review.
- Two look rows: sixteen clockwise directions, beginning at up.
- 73 occupied cells and 15 fully transparent unused cells.

The final PNG passed structural, chroma, jump, registration, and visual
direction checks. Three isolated reviewers confirmed the gaze axes. The
active WebP preserves every decoded RGBA pixel from that PNG; encoding adds
no new artwork, neutral cell, or animation frame.

## Source and active files

The original PNG and local host manifest are preserved in
`assets/original/peon`. The original account-pet ID and temporary upload
links are not part of the distribution. `assets/pet-revision.json` records
source and active hashes.

| File | SHA-256 |
|---|---|
| Original PNG | `d77132a73d2ccda9689ffe6417723fc5b0169688d9fb486e947e19f658920420` |
| Active WebP | `f8c7b8bd8c183f5ffe2ba30735a11b86994e8d7e67a3b73a85cc7137168cbaa4` |

The WebP was encoded with Pillow using `lossless=True`, `quality=100`,
`method=6`, and `exact=True`. Decoded pixels and transparent RGB were checked
after encoding. Native host rendering remains unverified.

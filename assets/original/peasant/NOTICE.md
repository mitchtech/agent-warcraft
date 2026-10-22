# Peasant pet artwork

This artwork depicts a Warcraft III-era human peasant. Michael J. Mitchell
requested it on October 22, 2026, and created it with Codex using built-in
image generation. A canonical character image grounded all animation strips
and look-direction strips. Deterministic extraction and shared registration
preserved the generated pixels while aligning character size, baselines,
and jump headroom. No game sprites, portraits, or models were extracted.

Warcraft and its characters belong to Blizzard Entertainment. This project
is not affiliated with or endorsed by Blizzard. Game audio has a separate
[rights notice](../../../audio/NOTICE.md).

The contributor's rights in this artwork are licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), as described in
[LICENSE.txt](LICENSE.txt). Suggested credit: "Peasant pet artwork by Michael
J. Mitchell / mitchtech, CC BY 4.0, https://github.com/mitchtech/agent-warcraft."

## Format and validation

- ID: `peasant`; display name: `Peasant`; sprite version: `2`.
- Transparent RGBA WebP, 1536 x 2288 pixels, with 192 x 208 cells.
- Nine distinct animation rows and sixteen clockwise look directions.
- 73 occupied cells and 15 fully transparent unused cells.

The final PNG passed structural, chroma, jump, registration, and visual
semantic checks. Three isolated reviewers checked the gaze axes. The active
WebP preserves every decoded RGBA pixel from the validated PNG. Native host
rendering remains unverified.

## Source and active files

The exact source PNG and local host manifest are preserved in
`assets/original/peasant`. `assets/peasant-pet-revision.json` records source,
active, and nine-row web-export hashes. Account-pet IDs and temporary upload
links are excluded from distribution.

| File | SHA-256 |
|---|---|
| Original PNG | `5c74965da31b1459a4f1401001533dfc427e9ea5c957587ffefdc23408963c24` |
| Active WebP | `5d6a5d6f406ed081a5897641c66abcc27279d7bd8cf29b8ad38bee524ae9f6bc` |

The WebP was encoded with Pillow using `lossless=True`, `quality=100`,
`method=6`, and `exact=True`. The web export preserves the first nine rows
and omits the local bundle's two look-direction rows.

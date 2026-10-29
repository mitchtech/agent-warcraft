# Community listing drafts

Drafts only. Nothing here has been submitted. The owner reviews each
destination's current rules, eligibility, and format before submitting from
their own account, one listing at a time. Skip any destination that does not
accept self-submitted projects, hook-only plugins, or projects that bundle
third-party game audio.

## Automatic discovery (no submission)

- **Gemini CLI extension gallery.** The `gemini-cli-extension` topic plus the
  root `gemini-extension.json` make the repository eligible; listing follows the
  gallery's validation and crawl schedule.
  [Requirements](https://geminicli.com/docs/extensions/releasing/)
- **GitHub topic pages.** `claude-code-plugin`, `codex-plugin`, `codex-pet`,
  `warcraft`, and the other repository topics surface it on GitHub's topic pages.

## Curated lists

For "awesome" lists of Claude Code plugins, hooks, or agent tooling, follow each
list's contributing guide (alphabetical placement, one line, no marketing
superlatives). Suggested entry:

```markdown
- [Agent Warcraft](https://github.com/mitchtech/agent-warcraft) - Warcraft III peon and peasant sound cues for Claude Code, Codex, and Gemini CLI hooks, with status-line gold and food meters and native Codex pets.
```

Category guidance: "Hooks" or "Notifications" where available; otherwise
"Plugins". For lists of Codex pets, use the pet entry instead:

```markdown
- [Agent Warcraft Peon and Peasant](https://github.com/mitchtech/agent-warcraft#codex-pets) - Two v2 Codex pets with nine animations and sixteen look directions, CC BY 4.0.
```

Mention the sibling projects only if the list groups related projects.

## Plugin directories

Some community directories index Claude Code and Codex plugin marketplaces.
Suggested short description (under 160 characters):

> Warcraft III sound cues for coding agents: Work complete, we need more gold,
> and we're under attack. Horde, Alliance, or both.

Suggested long description:

> Agent Warcraft plays original Warcraft III voice lines on Claude Code, Codex,
> and Gemini CLI events: "Ready to work." at session start, "Work, work." per
> prompt, a cue for approvals, "We're under attack!" for destructive commands,
> and "Work complete!" or "Job's done!" when a turn ends. Claude Code rate limits
> play "We need more gold!", and an optional status-line command shows usage as
> gold and the context window as food ("Build more farms." near the cap). Pick
> the Horde, the Alliance, both, a random faction per session, or duo mode.
> Native Peon and Peasant Codex pets install separately. Local, no telemetry,
> no runtime dependencies, never approves or blocks actions.

Install snippet for directories that show one:

```bash
claude plugin marketplace add mitchtech/agent-warcraft
claude plugin install warcraft@agent-warcraft
```

OpenAI's public plugin submission excludes lifecycle-hook plugins, so do not
submit there; the GitHub marketplace commands are the Codex distribution path.

## Notes for every listing

- Use the repository URL or the Pages site as the single link.
- Do not use Blizzard logos, portraits, or screenshots; the social card, the
  original pet art, and the waveform GIFs are the visuals.
- State the audio rights position plainly if asked: the clips belong to
  Blizzard Entertainment and are excluded from the MIT license.
- Record each submission in [campaign.csv](campaign.csv).

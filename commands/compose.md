---
description: Package a story with matched visual assets, usage rights, platform-ready crops, and archival context. One brief in, one publishable package out. Saves the package to your archive.
argument-hint: "earthquake Noto Peninsula" or paste a story draft
---

# /compose

Take a story and make it publishable.

## Trigger

Use when a story needs visual assets, context, and platform-ready formats before it can go live. Use when breaking news hits and you need a context package fast. Use when someone says "package this."

## Inputs

- **Story or topic** — required. One sentence to a full draft.
- **Platforms** — optional. Which crops to generate. Default: hero 16:9, social 1:1, story 9:16, thumbnail.
- **Archive depth** — optional. "Last 6 months" or "all time." Default: all time.

## Workflow

Follow the Reasoning Loop in the composer skill:

1. Read the brief — identify subject, entities, visual needs, time sensitivity
2. Search visual assets — tag search + visual search + derivative generation (parallel)
3. Search archive — prior coverage, sources, background, prior packages (parallel)
4. Search web context — competitive landscape, key facts, undercovered angles (parallel)
5. Assemble package — combine all findings into structured output
6. Save package to archive — write the package as a named doc so future runs compound

Each layer runs with what is connected. Missing connectors are noted in the package output, not used as a reason to stop or prompt for setup before delivering results.

## Output

Return the full package inline. Use the output format from the composer skill.

If the environment supports rich display, present as a tabbed interface:
- Tab 1: Historical context (archive + web findings + key stats)
- Tab 2: Visual assets (image grid with metadata + derivatives)
- Tab 3: Ready package (deliverables checklist with status indicators)
- Tab 4: How it works (numbered workflow steps)

## Quality Gates

✓ All included assets have photographer credit
✓ All included assets have rights status checked
✓ Expired or unclear rights flagged and excluded
✓ Derivatives generated or noted unavailable (not implied) for all specified platforms
✓ Archive searched if archive system detected
✓ Web context included
✓ Lead image recommended with reasoning
✓ Package status clearly stated: FULLY COMPOSED / COMPOSED WITH GAPS
✓ Package saved to archive if archive system supports file creation

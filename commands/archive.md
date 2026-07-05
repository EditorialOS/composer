---
description: Search your publication's archive for prior coverage, source lists, and institutional knowledge on a topic.
argument-hint: "earthquake Japan" or "boutique hotels Oaxaca"
---

# /archive

What have we already published about this?

## Trigger

Use when starting a new story and you need to know what the publication has already said. Use when you need source lists or background documents. Use when you want to avoid repeating an angle that's already been covered.

## Inputs

- **Topic** — required. What to search for.
- **Depth** — optional. "Last 6 months" or "all time." Default: all time.

## Workflow

1. Detect whether an archive system is connected by examining available MCP tool names. Look for tools that indicate file or document operations: search_files, list_files, get_file, create_file, write_file, or equivalent.

   If no archive system is detected, note the gap clearly and stop:
   > "No archive is connected. Add an archive system connector to .mcp.json to enable archive search. See CONNECTORS.md for setup."

2. Search the connected archive for:
   - Published stories containing the topic
   - Drafts and briefs related to the topic
   - Source lists and contact sheets
   - Background research documents
   - Editorial notes or post-mortems
   - Previously saved Composer packages on this topic
   - Any file that mentions the key entities

3. Group results by type.

4. If the search returns results but none are directly on topic, return the closest related material and note: "No direct coverage found on '[topic]'. Related material returned below."

5. If no results of any kind are found, note it explicitly: "This is the publication's first documented entry on this topic."

## Error Handling

- If archive search times out or fails: report "Archive search unavailable — connection error. Web context and visual assets still included below."
- If archive is connected but returns an access error on specific files: skip those files and note "N files inaccessible — check sharing permissions."

## Output

```
COMPOSER — ARCHIVE SEARCH
Generated: [date]
Topic: [topic]
Depth: [time range]

PUBLISHED COVERAGE
- [Title] — [date] — [angle taken] — [link]

SOURCES ON FILE
- [Name/org] — [context] — [from which document]

BACKGROUND DOCUMENTS
- [Document name] — [what it contains] — [link]

EDITORIAL NOTES
- [Lessons, cautions, institutional knowledge]

PRIOR COMPOSER PACKAGES
- [Package filename] — [date] — [brief summary]

SUMMARY
[N] published pieces | [N] sources | [N] background docs | [N] prior packages
Last coverage: [date of most recent piece on this topic]
```

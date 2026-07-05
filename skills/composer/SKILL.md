---
name: composer
description: "Story packaging methodology. Reads a brief, searches visual assets and archives, pulls web context, generates platform-ready crops, assembles a publishable package, and saves it to the archive. The production layer between 'story is done' and 'story is live.'"
---

# Composer — Story Packaging Methodology

## Purpose

Take a story and make it publishable. Not just written — packaged with matched visual assets, photographer credits, usage rights, platform-ready crops, archival context, and competitive landscape. One brief in, one package out. Every package saved back to the archive so the next run compounds.

## Core Principle

Every AI editorial tool stops at text. The 45 minutes between "the story is done" and "the story is live" — finding photos, cropping for each platform, checking rights, hunting for that background piece from six months ago — is the bottleneck nobody else solves. Composer closes that gap.

## Connector Detection

At the start of every run, identify what is connected by examining the tools each MCP server exposes — not by a configuration category. Categories are not acted on at runtime; tool capabilities are.

**Visual asset server:** Exposes tools whose names or descriptions indicate image library operations — search, find, assets, images, media, crop, transform, thumbnail, similarity, or equivalent. If a connected server exposes these, treat it as the visual asset system.

**Archive server:** Exposes tools whose names or descriptions indicate file or document operations — search_files, list_files, get_file, create_file, read_file, write_file, or equivalent. If a connected server exposes these, treat it as the archive system.

**Both:** Some systems (e.g. a CMS with media and docs) may qualify as both. Route accordingly.

**Neither:** Web search only. Always available, no connector needed.

Log the detected configuration at the start of the run (internally, not surfaced to the user unless asked):
- Visual asset system: [server name or "none detected"]
- Archive system: [server name or "none detected"]

Use this map for all routing decisions throughout the run.

## Operating Principles

- Read the brief. Reason about what the story needs. Never ask the user to classify it.
- Search what is connected. Skip what is not. Never fail silently — note every gap explicitly in the package output.
- All included assets must have photographer credit and rights status checked.
- Produce a complete package, not a list of recommendations.
- If `/setup` has not been run, suggest it at the end as a convenience — not at the beginning as a gate. The first experience is a deliverable, not setup.
- Never reveal internal tool calls, connector names, or MCP routing to the user unless asked.
- Never stop due to a missing connector — always produce what is possible with what is connected.
- Save every package to the archive if an archive system is connected. This is not optional — it is what turns Composer from a stateless command into a compounding system.

## The Reasoning Loop

Every time Composer runs, it follows these steps:

### 1. READ THE BRIEF

Parse the input. Identify:
- Subject and key entities (people, places, organizations, events)
- Visual needs (what kind of images would serve this story)
- Time sensitivity (is this breaking, planned, or evergreen)
- Angle, if present
- Format context (feature, news, newsletter, social) — infer from length and language signals

Do not ask the user to classify the request. Reason about what this brief needs and proceed.

**Brief depth determines package depth:**

| Brief Type | What You Receive | Package Response |
|-----------|-----------------|-----------------|
| One-line topic | "earthquake Noto Peninsula" | Full search across all layers, broad results |
| Topic + angle | "boutique hotel opening, 12 rooms, rooftop bar" | Focused search, angle-matched assets |
| Full draft | Pasted 1,000-word article | Precision matching — visual assets paired to specific sections |
| Headline + subhead | Publication-ready title pair | Search tuned to the specific narrative promise |

The richer the input, the more precise the package. But even a two-word topic produces a usable result.

### 2. SEARCH VISUAL ASSETS (parallel with Steps 3 and 4)

Check if a visual asset server is detected (see Connector Detection above).

If detected:
- **Tag search:** Search assets with tags relevant to the subject. Always include metadata fields for photographer credit and usage context.
- **Visual similarity search:** If the system supports it, search with a text description of what the story needs visually. Use the system's default similarity threshold, or 0.2 if none is specified.
- **For top matches:** Pull full asset details including dimensions and media metadata.
- **Rights check:** For each match, check available metadata fields for: photographer, usage_rights, campaign or licensing context, expiration date.

If no visual asset server is detected: check if the archive server has an `images/` folder and search by filename keywords as a fallback. Note the limitation explicitly: "No visual asset library connected. Archive searched by filename only — no similarity search or automatic cropping. Connect a DAM, CMS, or image management system for full visual matching."

**Rights Classification:**

| Status | Definition | Action |
|--------|-----------|--------|
| CLEARED | Photographer credited, usage rights confirmed, not expired | Include in package |
| EXPIRING | Rights expire within 30 days | Include with warning |
| CHECK REQUIRED | Photographer on file but rights field empty or ambiguous | List separately — do not include in main package |
| EXPIRED | Rights expiration date has passed | Exclude entirely — list in "not used" section |
| UNKNOWN | No photographer or rights metadata on file | Exclude — list separately with note to verify before use |

Never fabricate asset metadata. If photographer or rights are not in the file, say "not on file." Never guess. The cost of a rights violation is orders of magnitude higher than the cost of flagging an unknown.

**Note on Photo Editor integration:** If your team uses Photo Editor, assets tagged at ingest already carry photographer, usage_rights, and expiration as XMP metadata. Composer reads those fields directly — the rights status arrives resolved with the asset.

- **Generate derivatives** for all assets with CLEARED or EXPIRING status using the crop or transform API your connected system provides. Target:

| Derivative | Ratio | Dimensions | Use |
|-----------|-------|------------|-----|
| Hero | 16:9 | 1920×1080 | Website header, featured image |
| Social | 1:1 | 1080×1080 | Instagram, Facebook, LinkedIn |
| Story | 9:16 | 1080×1920 | Instagram Stories, TikTok, vertical video |
| Thumbnail | 4:3 | 400×300 | Newsletter, search results, CMS preview |

If the connected system does not support on-the-fly cropping, note "Manual crop required" for each derivative and include the original asset URL. Do not imply crops were generated when they were not.

**Lead Image Selection:**

After searching, recommend the strongest lead image. Select based on:
1. Rights status (CLEARED preferred over EXPIRING)
2. Resolution (highest resolution among cleared assets)
3. Subject match (image content aligns with story angle, not just topic)
4. Color and composition (dominant colors that complement the story's tone)
5. Crop viability (works well in 16:9 hero without losing the subject)

State why this image leads. "Lead: highest-res cleared asset with strong subject-centered composition that crops well across all ratios."

**Error handling — visual assets:**
- Search returns zero results: report "No assets matched '[description]' in your library" and continue to remaining steps.
- System connected but search fails or times out: report "Visual asset search unavailable — connection error" and continue. Do not stop the full /compose run.
- Some derivatives fail to generate: include the original URL with "Manual crop required" noted for that derivative.
- No visual asset library detected: see fallback above.

### 3. SEARCH ARCHIVE (parallel)

If an archive server is detected (see Connector Detection above):
- Search for prior coverage on this subject and related topics, entities, and angles.
- Look for: published stories, source lists, contact sheets, background documents, editorial notes, prior briefs, and previously saved Composer packages.

**Archive Search Strategy:**

| Search Layer | What to Look For | Why It Matters |
|-------------|-----------------|---------------|
| Direct coverage | Stories on the same subject | Avoid repeating angles, build on prior reporting |
| Related entities | People, places, organizations connected to the subject | Surfaces context the writer may not know exists |
| Thematic overlap | Stories under the same editorial theme | Finds internal linking opportunities and narrative throughlines |
| Source lists | Contact information, expert quotes, prior interview subjects | Saves the writer from rebuilding a source list from scratch |
| Background docs | Research, data, notes from prior coverage | Institutional knowledge that would otherwise be lost |
| Prior packages | Previously saved Composer packages on this topic | Direct prior runs — angles already taken, assets already used |

Group findings by: Published coverage / Sources / Background / Editorial notes / Prior packages.

**First Coverage Detection:**
If this is the first time the publication has covered this topic, note it explicitly: "This is the publication's first documented entry on this topic. This package will become the first archive entry." First coverage is editorially significant — the writer is starting from zero, and the web context search becomes more important.

**Error handling — archive:**
- Archive connected but search times out: report "Archive search unavailable — connection error" and continue. Do not stop the full /compose run.
- Archive returns results but some files are inaccessible: skip those files and note "N files inaccessible — check sharing permissions."
- No results found at all: report first coverage status as above.

If no archive server is detected:
- Note: "No archive connected. Connect an archive system to enable archive search and package saving."

### 4. SEARCH WEB CONTEXT (parallel)

Always runs. No connector needed. Search for:
- Who else has covered this topic recently — specific publications and angles
- Key facts, data, timeline, historical context
- Trending angles and current discussion
- Competitive coverage landscape — what has been said vs. what hasn't

**Undercovered Angle Identification:**

The most valuable output of web context search is not what has been covered — it's what hasn't. Identify gaps:
- Angles no one has taken on a trending topic
- Data points that exist but haven't been synthesized into a narrative
- Local or niche perspectives missing from mainstream coverage
- Counter-arguments to the prevailing narrative

Flag these as: "Undercovered angle: [description]. No major publication has approached [topic] from [this perspective]."

### 5. ASSEMBLE PACKAGE

Combine all findings into a structured output:

```
COMPOSER — PACKAGE
Generated: [date and time]

BRIEF: [subject summary from Step 1]
TIME SENSITIVITY: [BREAKING / PLANNED / EVERGREEN]

---

VISUAL ASSETS

LEAD IMAGE: Asset [N] — [why this leads]

Asset 1: [display name]
  Source: [URL]
  Photographer: [from metadata, or "not on file"]
  Usage rights: [from metadata, or "not on file"]
  Rights status: [CLEARED / EXPIRING / CHECK REQUIRED / UNKNOWN]
  Derivatives:
    Hero (16:9):    [URL or "Manual crop required"]
    Social (1:1):   [URL or "Manual crop required"]
    Story (9:16):   [URL or "Manual crop required"]
    Thumbnail:      [URL or "Manual crop required"]

[Repeat for each matched asset]

ASSETS NOT USED
[Assets that matched but had unclear or expired rights — with reason]
[Or: "No visual asset library connected"]

---

ARCHIVE CONTEXT
[Prior coverage, sources, background from archive]
[Or: "No archive connected"]

---

MARKET CONTEXT
[Competitive coverage, key facts, timeline from web search]
[Undercovered angles identified]

---

DELIVERABLES READY
[Checklist of what's complete vs pending]

---

PACKAGE STATUS: [FULLY COMPOSED / COMPOSED WITH GAPS]
[If gaps: list which layers are missing and what connector would close them]
```

### 6. SAVE PACKAGE TO ARCHIVE

If an archive server is detected and supports file creation:

Save the assembled package as a document in the archive:
- **Filename:** `composer-[topic-slug]-[YYYY-MM-DD].md`
  Example: `composer-earthquake-noto-peninsula-2025-07-05.md`
- **Topic slug:** lowercase, hyphens, max 5 words from the subject
- **Location:** The archive folder if one was identified during the run; otherwise the root of the connected archive
- **Content:** The full package output from Step 5

After saving, append to the package output:
```
---
SAVED TO ARCHIVE: [filename]
Next /compose run on this topic will surface this package as prior coverage.
```

If the archive server is connected but does not support file creation (read-only): note "Archive is read-only — package not saved. Prior coverage search still available."

If no archive server is detected: skip silently (already noted in Step 3).

This write is what turns Composer from a stateless command into a compounding system. Every run becomes prior coverage for the next.

## Package Quality Assessment

A complete package has five layers. Rate each:

| Layer | Complete | Partial | Missing |
|-------|----------|---------|---------|
| Visual assets | 3+ cleared images with derivatives | 1-2 images or rights unchecked | No visual asset library connected |
| Lead image | Recommended with reasoning | Multiple candidates, no clear lead | No cleared assets |
| Archive context | Prior coverage found and summarized | Related content found, not directly on topic | No archive connected |
| Web context | Competitive landscape mapped, undercovered angles identified | Key facts found, no competitive analysis | Search returned no relevant results |
| Derivatives | All four crop ratios generated or noted for all cleared assets | Some crops generated | System does not support on-the-fly cropping |

A package with all five layers complete is FULLY COMPOSED. A package with 3-4 layers is COMPOSED WITH GAPS. Note which layers are missing and what the user would need to connect to complete them.

## Connector Awareness

| Connector | If Available | If Unavailable |
|-----------|-------------|----------------|
| Visual asset server (detected by tool capabilities) | Visual search, rights checking, derivative generation — capability varies by system | Filename search in archive images/ folder only. No similarity search. Note manual crop required for all assets. |
| Archive server (detected by tool capabilities) | Archive search: prior coverage, source lists, background documents. Package saved after each run. | No archive layer. Package still runs without historical context. No package saving. |
| Web search | Always available | — |

### Degradation Behavior

Composer works with whatever is connected. The package adapts:

| Connected | Package Includes |
|-----------|-----------------|
| Visual asset system + archive + web | Full package — all five layers + package saved to archive |
| Archive + web (no visual system) | Archive + market context + package saved. Visual assets section notes the gap. |
| Visual asset system + web (no archive) | Visual assets + market context. Archive section notes the gap. No package saving. |
| Web only (nothing else) | Market context + undercovered angles. Visual and archive sections note gaps. Still useful — competitive landscape alone is worth the command. |

The first experience should always be a deliverable, not a setup prompt. Even with zero connectors, `/compose earthquake Noto Peninsula` returns a market context package with competitive coverage and undercovered angles.

## What Composer Never Does

- Never fabricates asset metadata — if photographer or rights are not in the file, say "not on file"
- Never includes assets with EXPIRED rights in the main package
- Never stops a /compose run because a connector is missing — always deliver what's possible
- Never asks the user to classify a brief — reads it and reasons
- Never reveals internal tool calls, connector names, or MCP routing to the user
- Never presents a setup wall before the first deliverable — show what's possible, then suggest setup at the end
- Never implies crops were generated when the system does not support on-the-fly transforms
- Never routes on configuration categories — detects capabilities from exposed tool names at runtime

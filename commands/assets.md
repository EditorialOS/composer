---
description: Search your visual asset library for images that match a story or topic. Returns matched images with photographer credits, usage rights, and platform-ready crops where your connected system supports them.
argument-hint: "coastal Japan landscape" or "food photography warm tones"
---

# /assets

Find the right visuals for a story.

## Trigger

Use when you need images for a story, post, or campaign. Use when you want to know what's in your library before commissioning new photography.

## Inputs

- **Description** — required. What the story is about, or what kind of image you need.
- **Tags** — optional. Specific tags to search. Default: infer from description.
- **Platforms** — optional. Which crops to generate. Default: all four (hero, social, story, thumbnail).

## Workflow

1. Detect whether a visual asset system is connected by examining available MCP tool names. Look for tools that indicate image library operations: search, assets, images, media, crop, transform, thumbnail, similarity search, or equivalent.

   If no visual asset system is detected, note the gap clearly and stop:
   > "No visual asset library is connected. Add a DAM, CMS, or image management system connector to .mcp.json to enable asset search. See CONNECTORS.md for setup."

2. If detected, search using whatever methods the system's tools support:
   a) **Tag search** — search assets with tags relevant to the description. Include photographer and usage rights metadata fields.
   b) **Visual similarity search** — if the system supports it, search by description text. Use the system's default similarity threshold, or 0.2 if none is specified.
   c) If only one method is available, use it and note the limitation.

3. For each result, check metadata for:
   - `photographer` or equivalent credit field
   - `usage_rights` or equivalent rights field
   - `campaign` or licensing context
   - `expiration` or rights expiry date

   Flag any assets with unclear, missing, or expired rights.

4. For assets with CLEARED rights, generate platform derivatives using the URL transform or crop API your connected system provides. Target dimensions:
   - Hero 16:9: 1920×1080
   - Social 1:1: 1080×1080
   - Story 9:16: 1080×1920
   - Thumbnail 4:3: 400×300

   If your connected system does not support on-the-fly cropping, note "Manual crop required" for every derivative and include the original asset URL. Do not imply crops were generated.

5. Recommend a lead image with reasoning.

## Error Handling

- If the asset search returns zero results: report "No assets matched '[description]' in your library. Try broader keywords or check your library's tag vocabulary."
- If the system returns results but none have rights metadata: include all assets flagged as UNKNOWN rights, grouped separately with a note to verify before use.
- If crop generation fails for a specific asset: include the original URL and note "Manual crop required."

## Output

```
COMPOSER — ASSET SEARCH
Generated: [date]
Query: [description]

LEAD IMAGE: Asset [N] — [why this leads]

MATCHED ASSETS

Asset 1: [display name]
  Source: [URL]
  Photographer: [credit or "not on file"]
  Rights: [CLEARED / EXPIRING / CHECK REQUIRED / EXPIRED / UNKNOWN]
  Tags: [tags]
  Dimensions: [width x height]
  Derivatives:
    Hero (16:9):    [URL or "Manual crop required"]
    Social (1:1):   [URL or "Manual crop required"]
    Story (9:16):   [URL or "Manual crop required"]
    Thumbnail:      [URL or "Manual crop required"]

[Repeat for each matched asset]

NOT USABLE (rights issues):
[List with reason]

SUMMARY
[Total matched] | [Rights cleared] | [Flagged]
```

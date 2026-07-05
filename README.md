# Composer

Package stories with matched visual assets, usage rights, platform-ready crops, and archival context.

Every editorial AI tool stops at text. Composer picks up where they leave off — the 45 minutes between "the story is done" and "the story is live."

One brief in. One publishable package out.

## Commands

**`/compose`** — Full package. Searches your visual library for matched assets, pulls prior coverage from your archive, researches the competitive landscape, generates platform-ready crops where your connected system supports it, and assembles everything into a publishable package. Saves the package to your archive so every run compounds.
```
/compose earthquake Noto Peninsula
/compose boutique hotel opening Oaxaca, 12 rooms, rooftop mezcal bar
/compose [paste a full brief or draft]
```

**`/assets`** — Visual asset search only. Find matched images with photographer credits, usage rights, and crops for every platform (where your system supports it).
```
/assets coastal Japan landscape
/assets food photography warm earth tones
/assets hotel interior courtyard architecture
```

**`/archive`** — Archive search only. What has your publication already covered on this topic? Prior stories, source lists, background documents, institutional knowledge.
```
/archive earthquake Japan
/archive boutique hotels Mexico
/archive shoulder season travel
```

**`/setup`** — Check which connectors are active and what Composer can do with your current configuration.

## How It Works

Composer reads a brief and reasons about what the story needs. Then it searches three layers simultaneously:

**Visual assets** — Your connected visual asset library (DAM, CMS media library, or image management system). Returns matched images with photographer credits and usage rights from metadata. Generates hero (16:9), social (1:1), story (9:16), and thumbnail crops where your connected system supports on-the-fly transforms. Notes "Manual crop required" where it does not.

**Archive** — Search for prior coverage on this topic. Surfaces past stories, source lists, background documents, and institutional knowledge. The context that would take a reporter 30 minutes to find manually. Every `/compose` run saves its package back to the archive — so the system compounds: each run becomes prior coverage for the next.

**Web context** — Competitive landscape, key facts, historical context, trending angles. Identifies undercovered angles — editorial opportunities nobody has taken yet.

Everything assembles into one structured package with a clear status: what's complete, what's pending, and why.

## Connectors

Both optional. Composer adapts to what's available.

| Connected | What you get |
|-----------|-------------|
| Nothing | Market context from web search |
| Archive system | + archive context (prior coverage, sources) |
| Visual asset system | + visual assets with rights and crops |
| Both | Full publishable package |

Connector setup details in `CONNECTORS.md`.

## What It Looks Like

**Breaking news:** Editor types `/compose earthquake Noto Peninsula` — gets a context package with historical coverage, key stats, competitive landscape, matched visual assets with rights-cleared crops, and identified angles nobody else has covered. Minutes, not hours.

**Hotel launch:** Editor types `/compose boutique hotel opening Oaxaca` — gets a seven-property competitive set, editorial angle assessment, matched photography with platform crops, and a deliverables checklist.

**Routine story:** Writer types `/compose shoulder season travel guide` — gets prior coverage from the archive, competitive positioning, matched visuals, and a gap analysis showing what hasn't been said yet.

## Works With Photo Editor

Composer and Photo Editor form a closed loop.

Photo Editor runs at ingest: it embeds photographer credit, usage rights, and expiration dates directly into every image file as XMP metadata. Composer runs at publish: its rights check reads exactly those fields — photographer, usage_rights, expiration — to classify each asset as CLEARED, EXPIRING, CHECK REQUIRED, or EXPIRED.

The loop is: Photo Editor writes the rights record into the file at shoot time. Composer reads it at publish time. No separate rights database. No manual lookup. The metadata travels with the image.

If your team uses Photo Editor, every asset tagged at ingest arrives at Composer with its rights status already resolved.

## Support

Questions or feedback: [github.com/EditorialOS/composer/issues](https://github.com/EditorialOS/composer/issues)

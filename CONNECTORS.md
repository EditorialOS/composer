# Connectors

Composer works with MCP connectors you configure in `.mcp.json`. Both are optional — the plugin adapts to what's available and notes every gap explicitly in the package output.

Composer detects what each connected server can do by examining the tools it exposes, not by a configuration category. Add a connector, and Composer will identify it as a visual asset system, an archive, or both, based on what operations it offers.

---

## Visual Asset Library — Your System of Record

**What it does:** Searches your image library by tags and visual similarity. Returns matched images with photographer credits, usage rights, and metadata. Generates platform-ready crops (hero, social, story, thumbnail) where your connected system supports on-the-fly transforms.

**Required for:** `/assets` command, visual asset matching in `/compose`

**Without it:** Composer still runs `/compose` using archive search and web context. Visual assets are noted as pending in the package.

### Connecting Your Visual Asset System

Composer works with any MCP-compatible visual asset system. Add your system's MCP server to `.mcp.json`:

```json
{
  "mcpServers": {
    "your-dam-or-cms": {
      "type": "http",
      "url": "https://your-system-mcp-endpoint/mcp"
    }
  }
}
```

Replace `"your-dam-or-cms"` with your connector name and `"url"` with the MCP endpoint your system provides.

**Compatible system types:**

| System Type | Examples |
|-------------|---------|
| Digital Asset Management (DAM) | Bynder, Widen Collective, Canto, Brandfolder, Extensis Portfolio |
| CMS media library | Contentful, WordPress (with MCP connector), Sanity |
| Cloud image management | Cloudinary, ImageKit, Cloudimage |
| File-based | Google Drive images folder (filename search only — no similarity search or auto-crop) |

### What Composer Uses From Your Visual Asset System

Composer reads asset metadata to make rights decisions. Best results when your assets have:

- **Tags** — descriptive topic, location, subject tags
- **Photographer** — credited in asset metadata
- **Usage rights** — rights status stored on the asset (cleared, licensed, restricted)
- **Expiration** — rights expiry date if applicable
- **Visual search** — if your system supports similarity search, enable it for richer matching

Without these fields, Composer can still find assets by tag or keyword, but rights checking will flag assets as UNKNOWN and exclude them from the package.

### Works With Photo Editor

If your team uses Photo Editor, assets tagged at ingest already carry photographer credit, usage rights, and expiration as XMP metadata. Composer's rights check reads those fields directly — no separate lookup required.

### Capability Differences by System Type

| System | Tag Search | Visual Similarity | Auto-Crop | Rights Check |
|--------|-----------|------------------|-----------|-------------|
| Full MCP DAM/CMS | ✓ | Depends on system | Depends on system | ✓ (if metadata present) |
| Google Drive (images folder) | Filename only | ✗ | ✗ | ✗ |

---

## Archive System — Content History

**What it does:** Searches your publication's connected archive for prior coverage, source lists, background documents, and institutional knowledge on any topic. Also receives saved packages from every `/compose` run — so the archive grows automatically.

**Required for:** `/archive` command, archival context in `/compose`, package saving

**Without it:** Composer still runs `/compose` using your visual asset library and web context. The archive section notes "no archive connected."

**Setup:** Add your archive system's MCP connector to `.mcp.json`. If you use Google Drive:

```json
{
  "mcpServers": {
    "google-drive": {
      "type": "http",
      "url": "https://your-drive-mcp-endpoint/mcp"
    }
  }
}
```

Connect Google Drive through your Claude settings and add its MCP endpoint above. Do not rely on a hardcoded URL — use the endpoint your connected Drive instance provides.

**Best results when your archive contains:**
- Past published stories (any format)
- Source lists and contact sheets
- Background research documents
- Editorial notes or post-mortems
- Prior briefs and pitches

---

## Web Search

**What it does:** Searches the open web for competitive coverage, key facts, historical context, and trending angles.

**Required for:** Market context in `/compose`

**Setup:** Built into Claude. No connector needed. Always available.

---

## Minimum Viable Composer

With no connectors at all, `/compose` still works — it runs web context search only and returns a market context package. Each connector you add unlocks another layer:

| Connected | What `/compose` returns |
|-----------|------------------------|
| Nothing | Market context only |
| Archive system | Market context + archive context + package saved to archive |
| Visual asset system | Market context + visual assets with crops |
| Both | Full package: visuals + archive + market context + package saved |

---
description: Check which connectors are active and configure Composer. Identifies your visual asset system and archive by the tools they expose. Optional — every command also works without setup and will note what's missing.
---

# /setup

Check what's connected. Composer adapts to what's available.

## Trigger

Run when first installing the plugin, or when a command reports a missing connector.

## Workflow

Composer identifies connectors by examining what tools each MCP server exposes — not by configuration categories. Configuration categories are not acted on at runtime.

1. **Detect visual asset system**

   List all available MCP tools. Identify any server whose tools indicate image library operations (search, assets, images, media, crop, transform, thumbnail, similarity search, or equivalent).

   - **Detected** — report the server name as active. Note total asset count and available capabilities (tag search, similarity search, auto-crop) based on what the server's tools expose.
   - **Not detected** — note as inactive. Explain that `/assets` and visual matching in `/compose` require a connected visual asset system. Direct the user to `CONNECTORS.md`.

2. **Detect archive system**

   Identify any server whose tools indicate file or document operations (search_files, list_files, get_file, create_file, write_file, or equivalent).

   - **Detected** — report the server name as active. Note whether file creation is supported (required for package saving). If a specific archive folder is not already known, ask the user which folder contains the publication's prior coverage.
   - **Not detected** — note as inactive. Explain that `/archive`, archival context in `/compose`, and package saving require an archive system.

3. **Report status**

```
COMPOSER — SETUP
Generated: [date]

CONNECTORS
  Visual asset system:  [✓ Connected ([server name], capabilities: tag search | similarity search | auto-crop) / ✗ Not detected]
  Archive system:       [✓ Connected ([server name], file creation: yes | read-only) / ✗ Not detected]

CAPABILITIES
  /compose       [Full / Partial — missing: visual assets | archive | both]
  /assets        [Available / Requires a connected visual asset system]
  /archive       [Available / Requires a connected archive system]
  Package saving [Available / Not available — archive not connected or read-only]

[If both connected:]
Composer is fully configured. Run /compose with any brief.

[If partial:]
Composer works with what's connected.
[List what's available and what's limited]
Add the missing connector to .mcp.json to unlock full capability. See CONNECTORS.md.

[If neither:]
Composer can still run /compose using web search only.
Add connectors to .mcp.json for visual assets and archive search. See CONNECTORS.md.
```

## Notes

- Setup is optional. Every command checks what's available and adapts.
- No config file is written. Composer detects connectors live on every run.
- This command exists for transparency — so users know what's active before running /compose.

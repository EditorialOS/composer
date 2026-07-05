# Changelog

## 1.0.1 — validate.py

- **Added `validate.py`.** A stdlib-only Python script that checks the plugin
  installation end-to-end: manifest completeness, required files, MCP config
  structure, Python environment, and connector detection. Runs standalone
  (`python3 validate.py`) with coloured pass/fail output and a `--json` flag
  for CI integration. Exit code 0 on all-pass, 1 on any failure.

## 1.0.0 — first public release

- **Complete plugin manifest.** `plugin.json` now includes `version`, `author`,
  `license`, `keywords`, `homepage`, and `repository` — matching the standard
  established by Photo Editor and ready for marketplace submission.
- **Capability detection replaces category routing.** `.mcp.json` no longer
  ships a hardcoded `category` field (which is not acted on at runtime). Composer
  now identifies visual asset and archive servers by examining the tools each
  connected MCP server exposes. This works correctly with any compliant connector,
  not just ones tagged with an unrecognized category field.
- **Drive endpoint removed.** The hardcoded `https://gdrive.mcp.claude.com/mcp`
  endpoint has been removed from `.mcp.json`. Users connect their archive system
  through their own MCP config and add the endpoint they control. `CONNECTORS.md`
  updated to remove the "pre-configured" claim.
- **Package persistence.** `/compose` now saves every package to the archive as
  a named document (`composer-[topic-slug]-[YYYY-MM-DD].md`) when an archive
  system is connected and supports file creation. Future `/compose` runs on the
  same topic surface prior packages in the archive step — turning Composer from
  a stateless command into a compounding system.
- **Honest crop language.** README and skill documentation now accurately describe
  crop generation as conditional: generated where the connected system supports
  on-the-fly transforms, noted as "Manual crop required" where it does not. No
  capability is implied that the degraded case does not deliver.
- **Photo Editor flywheel documented.** README and `CONNECTORS.md` now document
  the closed loop: Photo Editor writes photographer credit, usage rights, and
  expiration into image files as XMP at ingest; Composer reads those exact fields
  at publish. Teams using both plugins get rights status resolved automatically,
  with no separate lookup required.
- **Cross-plugin references removed.** README no longer references other plugins
  by name. Composer is documented as a standalone tool that also integrates with
  Photo Editor where relevant.
- **Contact convention aligned.** Support now routes to GitHub Issues, consistent
  with Photo Editor.

# PRD — Composer v1.0

  **Status:** Shipped · [Changelog](CHANGELOG.md)
  **Owner:** Roger Gurbani

  ---

  ## Problem

  Every story that's "done" still isn't publishable. Between the finished draft and the live piece sits unglamorous packaging work: finding the right visual assets, confirming usage rights, producing platform-specific crops, and capturing archival context so the piece is findable and reusable later. This takes skilled people roughly 45 minutes per story, it's nobody's favorite work, and when it's rushed, rights mistakes and unfindable assets are the result.

  ## Users

  - Editorial and content teams packaging stories for multi-platform publication
  - Photo desks and content ops roles that own asset selection and rights confirmation
  - Teams already running Editorial OS who need the last mile between draft and publish

  ## What v1 does

  - Takes one brief in and produces one publishable package out: story plus matched visual assets, usage rights, platform-ready crops, and archival context
  - Matches assets to the story from the connected library, reading embedded rights metadata rather than guessing
  - Produces platform-specific crop specifications per destination
  - Writes archival context so packaged stories remain findable and traceable
  - Degrades gracefully by connector level, documented per level

  ## What v1 explicitly does NOT do

  - **Does not edit or retouch images.** Pixel work belongs upstream; [Photo Editor](https://github.com/EditorialOS/photo-editor) handles metadata at ingest.
  - **Does not write or revise the story.** Drafting is Editorial OS's job; Composer packages what's approved.
  - **Does not adjudicate rights.** It reads the rights metadata embedded in assets and surfaces it. Granting or clearing rights is a human decision.
  - **Does not publish.** Output is a package staged for a human to ship; no direct CMS or platform posting.

  ## Success criteria

  - A complete package (assets + rights + crops + context) is produced from a single brief without re-prompting
  - Zero packages include an asset whose embedded rights metadata conflicts with the intended use — conflicts are surfaced, never silently passed
  - Packaging time drops from ~45 minutes of skilled labor to a review step <!-- RAJ: time yourself on 2–3 real packages and put the number here. -->
  - Cross-product loop verified: rights written by Photo Editor at ingest are correctly read by Composer at packaging <!-- RAJ: run the loop once end-to-end and note it here. -->

  ## Roadmap

  <!-- RAJ: list the one or two v1.1 items you actually intend, or delete this section. -->

  ## Decision log

  - **Read rights from embedded metadata, not a sidecar database** — the asset carries its own truth; packages stay correct even when assets move between systems
  - **Package for review, don't publish** — the human gate is where editorial judgment stays
  - **One brief in, one package out** — a single well-defined unit of work per run, consistent with per-command scoping across the Editorial OS suite
  
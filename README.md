# cosyncing.github.io

Official project site for [cosyncing](https://github.com/cosyncing/cosyncing) —
"Code anywhere. Sync everywhere."

## Layout

- `index.html` — self-contained landing page (no build step, no framework).
  Light/dark theme via `localStorage('cosyncing-site-theme')`, system
  preference by default.
- `demo/` — the client UI demo: Desktop, Web, and Phone sections showing
  real app captures in dark and light. Images follow the page theme toggle.
- `zh/`, `ja/`, `ko/`, `es/` — the same two pages per locale, each with its
  own `demo/`. The nav language menu and the `hreflang` set list all five;
  keep them in step when adding a locale. Page-relative links only, so the
  tree still works opened as files.
- `assets/icons/` — favicons and PWA icons, copied from the client
  (`apps/client/web/`).
- `assets/brand/` — logo SVGs, Open Graph image, and the slogan banners
  (`banner/`, 2400×1260, theme-aware; from `apps/client/assets/brand/marketing/`).
  Each locale has its own pair, rendered from the matching banner template.
- `assets/agents/` — agent pill images for the supported-agent strip.
- `assets/shots/demo/real/<mode>/` — screenshots of the running app
  (dark/light): `workspace`, `detail`, `sessions`, `chat`, `attention`.
- `assets/sync/` — the sync demo video (`sync-demo.mp4`, `sync-demo.gif`):
  app and agent CLI side by side through a take-over and a permission approval.
- `install.sh`, `install.ps1` — unchanged stable-release installers for the
  broker, supported desktop client, interactive setup and pairing.
- `install-server.sh`, `install-server.ps1` — unchanged broker-only installers;
  they place files and print the setup command without starting a service.
- `installers.json` — the mirrored release and its four source asset URLs.

## Screenshots and video

The demo uses reviewed captures from the real app running against a
deterministic fixture server with fictitious sessions and attention events.
Capture tooling and fixture data are maintained outside this published site;
the public demo contains only the resulting product captures.

## Preview locally

```bash
python3 -m http.server 8000
# open http://127.0.0.1:8000/
```

Asset paths are relative (`assets/…`, `demo/index.html`), so pages work both
from a web root and opened directly as files.

## Short installer URLs

GitHub Pages serves the four installer files directly from the repository root:

```bash
curl --proto '=https' --tlsv1.2 -fsSL https://cosyncing.com/install.sh | sh
```

```powershell
powershell -NoProfile -c "irm https://cosyncing.com/install.ps1 | iex"
```

Use `install-server.sh` or `install-server.ps1` at the same domain for a
broker-only installation. The [installer guide](https://github.com/cosyncing/cosyncing/blob/main/docs/installation/script-install.md)
documents platform support, unattended setup and upgrades.

These scripts **change with every release**. They embed the version, release
download URLs, public trust anchors and artifact digests. Merely promoting a new
GitHub release does not update the website. Never hand-edit these copies or
substitute an unrendered source template.

After each accepted stable broker promotion, run from this repository root
(Python 3.9 or newer; no extra packages or signing credentials):

```bash
python3 scripts/sync-installers.py
git diff -- install.sh install-server.sh install.ps1 install-server.ps1 installers.json
git add install.sh install-server.sh install.ps1 install-server.ps1 installers.json
git commit -m "Update stable broker installer mirror"
git push origin main
```

The helper resolves GitHub's latest release once, requires a stable
`broker-vX.Y.Z` tag, and downloads all four assets before replacing local files.
It checks the release identity and byte count without modifying script content.
It never executes installers, commits, pushes, or reads signing credentials.
The generated scripts contain public keys by design; private keys do not belong
in this repository.

Review changes before committing. This repository deploys GitHub Pages from
`main`; if branch protection requires a PR, merge the reviewed change through
that PR first. After deployment, check all four short URLs return script text
matching the promoted release assets, and check `https://cosyncing.com/installers.json`.
During the deployment delay, short URLs still serve the previous mirrored release;
`https://github.com/cosyncing/cosyncing/releases/latest/download/<name>` is the
direct fallback. A rollback restores all four scripts and `installers.json`
together from a reviewed website commit.

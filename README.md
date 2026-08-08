# cosyncing.github.io

Official project site for [cosyncing](https://github.com/cosyncing/cosyncing) —
"Code anywhere. Sync everywhere."

## Layout

- `index.html` — self-contained landing page (no build step, no framework).
  Light/dark theme via `localStorage('cosyncing-site-theme')`, system
  preference by default.
- `demo/` — the client UI demo: Desktop, Web, and Phone sections showing
  real app captures in dark and light. Images follow the page theme toggle.
- `assets/icons/` — favicons and PWA icons, copied from the client
  (`apps/client/web/`).
- `assets/brand/` — logo SVGs, Open Graph image, and the slogan banners
  (`banner/`, 2400×1260, theme-aware; from `apps/client/assets/brand/marketing/`).
- `assets/agents/` — agent pill images (Claude Code, Codex, OpenCode, Pi).
- `assets/shots/demo/real/<mode>/` — screenshots of the running app
  (dark/light): `workspace`, `detail`, `sessions`, `chat`, `attention`.
- `assets/sync/` — the sync demo video (`sync-demo.mp4`, `sync-demo.gif`):
  app and agent CLI side by side through a take-over and a permission approval.

## Screenshots and video

The demo uses reviewed captures from the real app running against a
deterministic fixture broker with fictitious sessions and attention events.
Capture tooling and fixture data are maintained outside this published site;
the public demo contains only the resulting product captures.

## Preview locally

```bash
python3 -m http.server 8000
# open http://127.0.0.1:8000/
```

Asset paths are relative (`assets/…`, `demo/index.html`), so pages work both
from a web root and opened directly as files.

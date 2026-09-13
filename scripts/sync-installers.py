#!/usr/bin/env python3
"""Mirror the current stable broker's four installers into the website root.

Run from the website repository root. This downloads files; it never executes
installers, edits their contents, commits changes, or publishes the website.
"""

import json
from pathlib import Path
import re
import tempfile
from urllib.request import Request, urlopen


REPOSITORY = "cosyncing/cosyncing"
NAMES = ("install.sh", "install-server.sh", "install.ps1", "install-server.ps1")
API = f"https://api.github.com/repos/{REPOSITORY}/releases/latest"


def fetch(url):
    request = Request(url, headers={"User-Agent": "cosyncing-site-installer-sync"})
    with urlopen(request, timeout=60) as response:
        return response.read()


def main():
    root = Path.cwd()
    if not (root / "index.html").is_file() or not (root / "README.md").is_file():
        raise SystemExit("Run from the website repository root.")
    release = json.loads(fetch(API))
    tag = release["tag_name"]
    if (release["draft"] or release["prerelease"]
            or not re.fullmatch(r"broker-v\d+\.\d+\.\d+", tag)):
        raise SystemExit("GitHub latest must be a stable broker-vX.Y.Z release.")
    version = tag.removeprefix("broker-v")
    base = f"https://github.com/{REPOSITORY}/releases/download/{tag}"
    assets = {asset["name"]: asset for asset in release["assets"]}
    with tempfile.TemporaryDirectory(prefix=".installer-sync-", dir=root) as staging:
        stage = Path(staging)
        for name in NAMES:
            asset = assets.get(name)
            if not asset or asset["browser_download_url"] != f"{base}/{name}":
                raise SystemExit(f"Missing or unexpected release asset: {name}")
            content = fetch(asset["browser_download_url"])
            source = content.decode("utf-8-sig")
            prefix = r"\$VERSION\s*=\s*" if name.endswith(".ps1") else "VERSION="
            if (len(content) != asset["size"]
                    or not re.search(rf"^{prefix}'{re.escape(version)}'\r?$", source, re.M)
                    or base not in source):
                raise SystemExit(f"Wrong release identity or incomplete asset: {name}")
            if re.search(r"-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----", source):
                raise SystemExit(f"Unexpected private key in {name}")
            (stage / name).write_bytes(content)

        # Download and validate the whole set before changing the website files.
        current = json.loads(fetch(API))
        if current["id"] != release["id"] or current["tag_name"] != tag:
            raise SystemExit("GitHub latest changed during download; run again.")
        for name in NAMES:
            (stage / name).replace(root / name)
        metadata = {
            "release": tag,
            "source": release["html_url"],
            "installers": {name: f"{base}/{name}" for name in NAMES},
        }
        (root / "installers.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"Mirrored four unchanged installers from {tag}.")
    print("Review the diff, commit and push, then verify the live cosyncing.com URLs.")


if __name__ == "__main__":
    main()

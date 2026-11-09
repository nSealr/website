#!/usr/bin/env python3
"""Build and package reviewed companion source. Never runs during the site build."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import zipfile

if len(sys.argv) != 3 or not re.fullmatch(r"[0-9a-f]{40}", sys.argv[2]):
    raise SystemExit("Usage: python3 scripts/package_companion.py /path/to/nsealr FULL_COMMIT")
source, commit = Path(sys.argv[1]).resolve(), sys.argv[2]
site = Path(__file__).resolve().parent.parent

def git(*args):
    return subprocess.check_output(["git", "-C", str(source), *args], text=True).strip()

if git("status", "--porcelain", "--untracked-files=all", "--", "companion"):
    raise SystemExit("Companion source must be clean.")
git("diff", "--exit-code", commit, "--", "companion", "LICENSE")
tree = git("rev-parse", f"{commit}:companion")
subprocess.run(["npm", "ci", "--ignore-scripts"], cwd=source / "companion", check=True)
subprocess.run(["npm", "run", "build"], cwd=source / "companion", check=True)
git("diff", "--exit-code", commit, "--", "companion", "LICENSE")
dist = source / "companion/dist"
common = ["app.js", "app.js.LEGAL.txt", "app.css", "index.html", "help.html",
          "THIRD_PARTY_LICENSES.txt", "fonts/Inter.woff2", "fonts/Inter-LICENSE.txt",
          "fonts/JetBrainsMono.woff2", "fonts/JetBrainsMono-OFL.txt"]
extension = common + ["manifest.json", "background.js", "content.js", "injected.js"]

def contents(root, names):
    result = {}
    for name in names:
        path = root / name
        if path.is_symlink() or not path.is_file():
            raise SystemExit(f"Missing regular build asset: {name}")
        result[name] = path.read_bytes()
    return result

web = contents(dist, common)
for built, original in [("index.html", "index.html"), ("app.css", "style.css")]:
    if web[built] != (source / "companion" / original).read_bytes():
        raise SystemExit(f"Build does not match source: {built}")
license_text = (source / "LICENSE").read_bytes()
web["LICENSE.txt"] = license_text
# Host navigation only. Runtime JavaScript/CSS and extension files remain exact.
footer = '<a href="help.html">How to use the companion</a>'
html = web["index.html"].decode()
if html.count(footer) != 1:
    raise SystemExit("Review the changed companion footer before packaging.")
web["index.html"] = html.replace(footer, footer + ' · <a href="/downloads/">Browser extensions</a> · <a href="/">nsealr.com</a>').encode()

def digest(data):
    return hashlib.sha256(data).hexdigest()

def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()

identity = {"repository": "https://github.com/nSealr/nsealr", "commit": commit,
            "companion_tree": tree, "version": json.loads((dist / "manifest.json").read_text())["version"]}
archives = {}
downloads = site / "public/downloads"
downloads.mkdir(parents=True, exist_ok=True)
for browser, directory in [("chromium", dist), ("firefox", dist / "firefox")]:
    files = contents(directory, extension)
    files["LICENSE.txt"] = license_text
    files["SOURCE.json"] = encoded({**identity, "files": {name: digest(data) for name, data in files.items()}})
    target = downloads / f"nsealr-{browser}.zip"
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    archives[target.name] = {"sha256": digest(target.read_bytes()), "bytes": target.stat().st_size}

target = site / "public/connect"
if target.exists():
    shutil.rmtree(target)
for name, data in web.items():
    path = target / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
(target / "source.json").write_bytes(encoded({**identity, "web": {name: digest(data) for name, data in web.items()}, "downloads": archives}))
print(f"Packaged {commit}: /connect/ and two extension ZIPs.")

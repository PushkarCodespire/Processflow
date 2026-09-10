#!/usr/bin/env python3
"""
Build the Teams app package (npi-operations-hub.zip) with the live URL baked in.

Usage:
    python build_teams_package.py https://<your-app>.vercel.app

Run this AFTER the site is live on Vercel. It reads teamsapp/manifest.json,
substitutes the host into contentUrl / configurationUrl / validDomains, writes
teamsapp/manifest.built.json, and zips that manifest + the two icons into
npi-operations-hub.zip (manifest + icons at the zip root, as Teams requires).
"""
import sys, os, json, zipfile
from urllib.parse import urlparse

if len(sys.argv) != 2:
    print("Usage: python build_teams_package.py https://<your-app>.vercel.app")
    sys.exit(1)

url = sys.argv[1].strip().rstrip("/")
host = urlparse(url).netloc or url.replace("https://", "").replace("http://", "").split("/")[0]

here = os.path.dirname(os.path.abspath(__file__))
tapp = os.path.join(here, "teamsapp")

with open(os.path.join(tapp, "manifest.json"), "r", encoding="utf-8") as f:
    manifest = f.read().replace("__APP_URL__", host)

json.loads(manifest)  # fail early if substitution broke JSON

built = os.path.join(tapp, "manifest.built.json")
with open(built, "w", encoding="utf-8") as f:
    f.write(manifest)

zip_path = os.path.join(here, "npi-operations-hub.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("manifest.json", manifest)          # manifest at zip root
    z.write(os.path.join(tapp, "color.png"), "color.png")
    z.write(os.path.join(tapp, "outline.png"), "outline.png")

print("Host baked in:      ", host)
print("Wrote manifest:     ", built)
print("Teams package:      ", zip_path)
print("Upload this zip in Teams -> Apps -> Manage your apps -> Upload a custom app")

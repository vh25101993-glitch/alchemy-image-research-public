#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
from pathlib import Path

import requests
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
BG = (243, 245, 247)
PRIMARY = 768
THUMB = 256
MAX_BYTES = 20 * 1024 * 1024


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fetch(url: str) -> tuple[bytes, str]:
    headers = {"User-Agent": "AlchemyChemistryImageBuilder/1.0"}
    with requests.get(url, headers=headers, timeout=60, stream=True) as r:
        r.raise_for_status()
        ctype = r.headers.get("content-type", "")
        if not ctype.startswith("image/"):
            raise RuntimeError(f"Not an image: {ctype} for {url}")
        chunks = []
        total = 0
        for chunk in r.iter_content(256 * 1024):
            if not chunk:
                continue
            total += len(chunk)
            if total > MAX_BYTES:
                raise RuntimeError(f"Source exceeds {MAX_BYTES} bytes")
            chunks.append(chunk)
    return b"".join(chunks), ctype


def square_contain(raw: bytes, size: int) -> Image.Image:
    with Image.open(io.BytesIO(raw)) as im:
        im.verify()
    with Image.open(io.BytesIO(raw)) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        fitted = ImageOps.contain(im, (size, size), method=Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (size, size), BG)
    canvas.paste(fitted, ((size - fitted.width)//2, (size - fitted.height)//2))
    return canvas


def save_webp(img: Image.Image, path: Path, max_bytes: int, start_quality: int):
    path.parent.mkdir(parents=True, exist_ok=True)
    quality = start_quality
    while quality >= 50:
        buf = io.BytesIO()
        img.save(buf, "WEBP", quality=quality, method=6)
        data = buf.getvalue()
        if len(data) <= max_bytes or quality == 50:
            path.write_bytes(data)
            return data, quality
        quality -= 4
    raise RuntimeError("Unable to encode WebP")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    args = ap.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = ROOT / manifest_path
    manifest = read_json(manifest_path)

    generated = []
    for entry in manifest["entries"]:
        sid = entry["canonical_substance_id"]
        raw, ctype = fetch(entry["download_url"])
        source_sha256 = hashlib.sha256(raw).hexdigest()

        primary_img = square_contain(raw, PRIMARY)
        thumb_img = square_contain(raw, THUMB)

        out = ROOT / "generated" / "substances" / sid
        primary_path = out / "primary.webp"
        thumb_path = out / "thumb.webp"
        primary_bytes, q1 = save_webp(primary_img, primary_path, 300_000, 82)
        thumb_bytes, q2 = save_webp(thumb_img, thumb_path, 60_000, 78)

        (out / "primary.webp.b64").write_text(base64.b64encode(primary_bytes).decode("ascii") + "\n", encoding="ascii")
        (out / "thumb.webp.b64").write_text(base64.b64encode(thumb_bytes).decode("ascii") + "\n", encoding="ascii")

        metadata = {
            "schema_version": 2,
            "canonical_substance_id": sid,
            "database_substance_id": entry["database_substance_id"],
            "formula": entry["formula_key"],
            "display_name_en": entry["display_name_en"],
            "asset_revision": 1,
            "files": {"primary": "primary.webp", "thumbnail": "thumb.webp"},
            "representation": {
                "visual_scope": entry["visual_scope"],
                "fit_mode": "contain",
                "background": "#F3F5F7",
                "primary_size": [PRIMARY, PRIMARY],
                "thumbnail_size": [THUMB, THUMB]
            },
            "provenance": {
                "source_type": "verified real photograph",
                "provider": "Wikimedia Commons",
                "source_page": entry["source_page_url"],
                "download_url": entry["download_url"],
                "source_file_title": entry["file_title"],
                "author": entry["author"],
                "license": entry["license"],
                "license_url": entry["license_url"],
                "source_content_type": ctype,
                "source_sha256": source_sha256,
                "verified_by": "ChatGPT manual web verification",
                "verified_date": "2026-09-30"
            },
            "asset_integrity": {
                "primary_sha256": hashlib.sha256(primary_bytes).hexdigest(),
                "thumbnail_sha256": hashlib.sha256(thumb_bytes).hexdigest(),
                "primary_bytes": len(primary_bytes),
                "thumbnail_bytes": len(thumb_bytes),
                "primary_webp_quality": q1,
                "thumbnail_webp_quality": q2
            },
            "chemistry_authority": "database only; this file is visual metadata"
        }
        write_json(out / "metadata.json", metadata)
        generated.append(metadata)
        print(f"BUILT {sid}: primary={len(primary_bytes)} thumb={len(thumb_bytes)}")

    write_json(ROOT / "generated" / "manifest.json", {
        "schema_version": 1,
        "source_manifest": str(manifest_path.relative_to(ROOT)),
        "count": len(generated),
        "entries": generated
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

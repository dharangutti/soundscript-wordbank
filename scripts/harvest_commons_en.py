#!/usr/bin/env python3
"""Harvest CC0 / CC-BY (non-SA) English pronunciations from Wikimedia Commons."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS_ROOT = ROOT / "corpus" / "v2026.07"
AUDIO_DIR = CORPUS_ROOT / "audio" / "en"
LEMMAS_PATH = CORPUS_ROOT / "en" / "lemmas.json"
SOURCES_PATH = CORPUS_ROOT / "en" / "SOURCES.md"

USER_AGENT = "SoundScriptWordbankBot/1.0 (https://github.com/dharangutti/soundscript-wordbank; corpus harvest)"

# Curated word → Commons filename. Licenses verified non-SA (CC0, Public domain, or CC-BY).
HARVEST_MANIFEST: dict[str, str] = {
    "another": "En-uk-another.ogg",
    "away": "En-uk-away.ogg",
    "beautiful": "En-uk-beautiful.ogg",
    "before": "En-us-before.ogg",
    "child": "En-uk-child.ogg",
    "computer": "En-uk-computer.ogg",
    "food": "En-uk-food.ogg",
    "friend": "En-uk-friend.ogg",
    "happy": "En-uk-happy.ogg",
    "hello": "En-us-hello.ogg",
    "it": "En-uk-it.ogg",
    "jingle": "En-us-jingle.ogg",
    "life": "En-uk-life.ogg",
    "little": "En-uk-little.ogg",
    "love": "En-uk-love.ogg",
    "man": "En-uk-man.ogg",
    "music": "En-uk-music.ogg",
    "people": "En-uk-people.ogg",
    "school": "En-uk-school.ogg",
    "sound": "En-us-sound.ogg",
    "star": "En-uk-star.ogg",
    "table": "En-uk-table.ogg",
    "this": "En-us-this.ogg",
    "together": "En-uk-together.ogg",
    "water": "En-uk-water.ogg",
    "way": "En-uk-way.ogg",
    "welcome": "En-uk-welcome.ogg",
    "with": "En-uk-with.ogg",
    "woman": "En-uk-woman.ogg",
    "work": "En-us-work.ogg",
}

# Lemmas without a standalone Commons clip yet — keep normalized WAV in-repo (CC0 pilot).
SUPPLEMENTAL_PILOT: dict[str, str] = {
    "test": "Pilot clip (v0.6.1) — no standalone CC-BY/CC0 Commons file found for lemma 'test'",
    "world": "Pilot clip (v0.6.1) — no standalone CC-BY/CC0 Commons file found for lemma 'world'",
}


def query_commons_file(filename: str) -> dict | None:
    title = f"File:{filename}"
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(
        {
            "action": "query",
            "titles": title,
            "prop": "imageinfo",
            "iiprop": "extmetadata|url",
            "format": "json",
        }
    )
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.load(response)

    page = next(iter(data["query"]["pages"].values()))
    if "missing" in page:
        return None

    info = page["imageinfo"][0]
    metadata = info["extmetadata"]
    return {
        "file": filename,
        "license": metadata.get("LicenseShortName", {}).get("value", ""),
        "license_url": metadata.get("LicenseUrl", {}).get("value", ""),
        "artist": metadata.get("Artist", {}).get("value", ""),
        "url": info.get("url", ""),
    }


def license_allowed(license_name: str) -> bool:
    if not license_name:
        return False
    lowered = license_name.lower()
    if "public domain" in lowered or lowered == "cc0":
        return True
    if "by-sa" in lowered:
        return False
    return lowered.startswith("cc by") or "creativecommons.org/licenses/by/" in lowered


def normalize_license(license_name: str) -> str:
    lowered = license_name.lower()
    if "public domain" in lowered or lowered == "cc0":
        return "CC0-1.0"
    return "CC-BY-4.0"


def strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text).strip()


def download_ogg(filename: str, destination: Path) -> None:
    url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{urllib.parse.quote(filename)}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        destination.write_bytes(response.read())


def convert_to_wav(source: Path, destination: Path) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-i",
            str(source),
            "-ar",
            "44100",
            "-ac",
            "1",
            "-sample_fmt",
            "s16",
            str(destination),
        ],
        check=True,
    )


def build_lemma_entry(lemma: str, info: dict) -> dict:
    license_code = normalize_license(info["license"])
    artist = strip_html(info.get("artist", ""))
    attribution = artist or f"Wikimedia Commons speaker; file {info['file']}"
    return {
        "lemma": lemma,
        "license": license_code,
        "source": f"Wikimedia Commons — {info['file']}",
        "attribution": attribution,
        "audio": f"audio/en/{lemma}.wav",
        "trimStartMs": 0,
        "gain": 1.0,
    }


def append_supplemental_pilot_entries(document: dict) -> list[dict]:
    """Keep pilot WAV clips for lemmas that lack a standalone Commons pronunciation."""
    existing = {entry["lemma"] for entry in document["entries"]}
    added: list[dict] = []

    for lemma, note in SUPPLEMENTAL_PILOT.items():
        if lemma in existing:
            continue
        wav_path = AUDIO_DIR / f"{lemma}.wav"
        if not wav_path.is_file():
            continue
        added.append(
            {
                "lemma": lemma,
                "license": "CC0-1.0",
                "source": note,
                "attribution": "SoundScript project (pilot placeholder pending harvest)",
                "audio": f"audio/en/{lemma}.wav",
                "trimStartMs": 0,
                "gain": 1.0,
            }
        )

    return added


def write_sources(entries: list[dict]) -> None:
    lines = [
        "# English pronunciation sources (v2026.07)",
        "",
        "Harvested via `scripts/harvest_commons_en.py`. Licenses: CC0-1.0 or CC-BY only (no CC-BY-SA).",
        "",
        "| Lemma | License | Commons file |",
        "|-------|---------|--------------|",
    ]
    for entry in sorted(entries, key=lambda item: item["lemma"]):
        file_name = entry["source"].split("—", 1)[-1].strip()
        url = f"https://commons.wikimedia.org/wiki/File:{urllib.parse.quote(file_name)}"
        lines.append(
            f"| `{entry['lemma']}` | {entry['license']} | [{file_name}]({url}) |"
        )
    lines.extend(
        [
            "",
            "See [LICENSE-POLICY.md](../../../LICENSE-POLICY.md).",
            "",
        ]
    )
    SOURCES_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    temp_dir = ROOT / ".harvest-tmp"
    temp_dir.mkdir(exist_ok=True)

    entries: list[dict] = []
    errors: list[str] = []

    for lemma, filename in sorted(HARVEST_MANIFEST.items()):
        print(f"Harvesting {lemma} ← {filename} ...", flush=True)
        try:
            info = query_commons_file(filename)
            time.sleep(0.15)
            if info is None:
                errors.append(f"{lemma}: file not found on Commons ({filename})")
                continue
            if not license_allowed(info["license"]):
                errors.append(f"{lemma}: license rejected ({info['license']})")
                continue

            ogg_path = temp_dir / filename
            wav_path = AUDIO_DIR / f"{lemma}.wav"
            download_ogg(filename, ogg_path)
            convert_to_wav(ogg_path, wav_path)
            entries.append(build_lemma_entry(lemma, info))
        except Exception as exc:  # pragma: no cover - harvest diagnostics
            errors.append(f"{lemma}: {exc}")

    if not entries:
        print("No entries harvested.", file=sys.stderr)
        return 1

    document = {
        "$schema": "../../../schema/lemmas.schema.json",
        "corpusId": "2026.07",
        "locale": "en",
        "version": 2,
        "status": "pilot",
        "description": "Harvested CC0/CC-BY English pronunciations from Wikimedia Commons.",
        "entries": entries,
    }
    LEMMAS_PATH.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    write_sources(entries)

    supplemental = append_supplemental_pilot_entries(document)
    if supplemental:
        document["entries"].extend(supplemental)
        document["entries"] = sorted(document["entries"], key=lambda item: item["lemma"])
        LEMMAS_PATH.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
        write_sources(document["entries"])

    print(f"\nHarvested {len(entries)} pronunciations → {AUDIO_DIR}")
    if errors:
        print("\nWarnings:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

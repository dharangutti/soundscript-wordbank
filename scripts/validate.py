#!/usr/bin/env python3
"""Validate SoundScript wordbank JSON data files against schemas."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover
    print("Missing dependency: jsonschema. Install with: pip install -r scripts/requirements.txt", file=sys.stderr)
    raise SystemExit(2) from exc

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "schema"

FILE_SCHEMAS = {
    "functionWords": "function-words.schema.json",
    "stressPrefixes": "stress-prefixes.schema.json",
    "wordProsody": "word-prosody.schema.json",
    "graphemeRules": "grapheme-rules.schema.json",
    "legalOnsets": "legal-onsets.schema.json",
    "syllabification": "syllabification.schema.json",
    "phonemeCompose": "phoneme-compose.schema.json",
    "phonemeWave": "phoneme-wave.schema.json",
    "phonemeTimbre": "phoneme-timbre.schema.json",
    "wordEntries": "word-entries.schema.json",
}


def load_json(path: Path) -> object:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_file(data_path: Path, schema_path: Path) -> list[str]:
    schema = load_json(schema_path)
    data = load_json(data_path)
    validator = Draft202012Validator(schema)
    return [f"{data_path}: {error.message}" for error in validator.iter_errors(data)]


def collect_function_words(data: dict) -> set[str]:
    words: set[str] = set()
    for items in data.get("categories", {}).values():
        words.update(item.lower() for item in items)
    return words


def cross_validate_locale(locale_dir: Path) -> list[str]:
    errors: list[str] = []

    locale_manifest = load_json(locale_dir / "locale.json")
    files = locale_manifest["files"]

    for key, relative in files.items():
        target = locale_dir / relative
        if not target.exists():
            errors.append(f"Missing locale file referenced by locale.json ({key}): {target}")

    function_words = load_json(locale_dir / files["functionWords"])
    all_function_words = collect_function_words(function_words)

    word_entries = load_json(locale_dir / files["wordEntries"])
    for entry in word_entries.get("entries", []):
        word = entry["word"].lower()
        if "category" in entry and entry["category"] == "function" and word not in all_function_words:
            errors.append(
                f"{locale_dir / files['wordEntries']}: word '{entry['word']}' marked function but not in function-words"
            )

        syllables = entry.get("syllables", [])
        stress = entry.get("stress", [])
        if syllables and stress and len(syllables) != len(stress):
            errors.append(
                f"{locale_dir / files['wordEntries']}: word '{entry['word']}' syllables/stress length mismatch"
            )

    compose = load_json(locale_dir / files["phonemeCompose"])
    wave = load_json(locale_dir / files["phonemeWave"])
    timbre = load_json(locale_dir / files["phonemeTimbre"])
    compose_phonemes = {item["phoneme"] for item in compose["phonemes"]}
    wave_phonemes = {item["phoneme"] for item in wave["phonemes"]}
    timbre_phonemes = {item["phoneme"] for item in timbre["phonemes"]}
    if compose_phonemes != wave_phonemes:
        missing_in_wave = sorted(compose_phonemes - wave_phonemes)
        missing_in_compose = sorted(wave_phonemes - compose_phonemes)
        if missing_in_wave:
            errors.append(f"Phoneme set mismatch: missing in wave table: {', '.join(missing_in_wave)}")
        if missing_in_compose:
            errors.append(f"Phoneme set mismatch: missing in compose table: {', '.join(missing_in_compose)}")

    if timbre_phonemes != compose_phonemes:
        missing = sorted(compose_phonemes - timbre_phonemes)
        if missing:
            errors.append(f"Timbre table missing phonemes: {', '.join(missing)}")

    graphemes = load_json(locale_dir / files["graphemeRules"])
    referenced_phonemes: set[str] = set()
    for rule in graphemes["digraphs"]:
        referenced_phonemes.update(rule["phonemes"])
    for rule in graphemes["singleLetters"]:
        referenced_phonemes.update(rule["phonemes"])
    special_letters = {rule["letter"] for rule in graphemes["singleLetters"]}
    for letter in "bdfghjklmnprstvwz":
        if letter not in special_letters:
            referenced_phonemes.add(letter)

    unknown = sorted(referenced_phonemes - compose_phonemes)
    if unknown:
        errors.append(f"Grapheme rules reference unknown phonemes: {', '.join(unknown)}")

    return errors


def validate_locale(locale_dir: Path) -> list[str]:
    errors: list[str] = []
    locale_manifest = load_json(locale_dir / "locale.json")
    files = locale_manifest["files"]

    errors.extend(validate_file(locale_dir / "locale.json", SCHEMA_DIR / "locale.schema.json"))
    for key, schema_name in FILE_SCHEMAS.items():
        relative = files[key]
        errors.extend(validate_file(locale_dir / relative, SCHEMA_DIR / schema_name))

    errors.extend(cross_validate_locale(locale_dir))
    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(validate_file(ROOT / "manifest.json", SCHEMA_DIR / "manifest.schema.json"))

    manifest = load_json(ROOT / "manifest.json")
    for locale in manifest["locales"]:
        locale_dir = ROOT / locale["path"]
        if not locale_dir.exists():
            errors.append(f"Missing locale directory: {locale_dir}")
            continue
        errors.extend(validate_locale(locale_dir))

    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    locale_count = len(manifest["locales"])
    print(f"All wordbank data files validated successfully ({locale_count} locale(s)).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# Manifest schema guide

Human-readable reference for wordbank manifest files. Machine validation lives in `schema/*.schema.json`.

## Root package manifest (`manifest.json`)

Describes the whole repository: locale packs, schema version, default locale.

```json
{
  "$schema": "./schema/manifest.schema.json",
  "name": "soundscript-wordbank",
  "version": "0.5.0",
  "schemaVersion": 1,
  "defaultLocale": "en",
  "locales": [
    { "code": "en", "name": "English", "path": "data/en" }
  ]
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `name` | yes | Package identifier (`soundscript-wordbank`) |
| `version` | yes | Semver of the entire package |
| `schemaVersion` | yes | Breaking schema generation; increment on incompatible JSON shape changes |
| `defaultLocale` | yes | BCP-47-style short code (`en`, `es`, `fr`) |
| `locales[]` | yes | Locale pack index |
| `locales[].path` | yes | Relative path to locale directory (`data/en`) |

## Locale manifest (`data/<locale>/locale.json`)

Index of files for one locale pack. Each `files.*` value is relative to the locale directory.

| File key | JSON file | Purpose |
|----------|-----------|---------|
| `functionWords` | `function-words.json` | Closed-class words |
| `stressPrefixes` | `stress-prefixes.json` | Prefix stress rules |
| `wordProsody` | `word-prosody.json` | Pitch/contour offsets |
| `graphemeRules` | `grapheme-rules.json` | Grapheme → phoneme |
| `legalOnsets` | `legal-onsets.json` | Syllable onset table |
| `syllabification` | `syllabification.json` | Locale syllabification rules |
| `phonemeCompose` | `phoneme-compose-gestures.json` | Compose gestures |
| `phonemeWave` | `phoneme-wave-frequencies.json` | Wave speech bands |
| `phonemeTimbre` | `phoneme-timbre-profiles.json` | Timbre profiles |
| `wordEntries` | `words/common.json` | Per-word overrides |

## Corpus manifest (`corpus/vYYYY.MM/manifest.json`)

Describes a large lemma snapshot. See [VERSIONING.md](VERSIONING.md).

```json
{
  "$schema": "../../schema/corpus-manifest.schema.json",
  "id": "2026.07",
  "version": 0,
  "status": "pilot",
  "locales": [
    {
      "code": "en",
      "path": "en",
      "lemmaFile": "lemmas.json",
      "pilotFile": "pilot-1k.txt"
    }
  ],
  "engineCompatibility": {
    "soundscriptMin": "8.0.0",
    "wordbankMin": "0.5.0"
  }
}
```

| Field | Description |
|-------|-------------|
| `id` | Corpus month `YYYY.MM` |
| `version` | Patch integer within the month (`0` → `2026.07.0`) |
| `status` | `pilot`, `draft`, or `released` |
| `locales[].pilotFile` | Curated lemma list (text, one lemma per line) before harvest |
| `locales[].lemmaFile` | Harvested lemma JSON (may start empty) |

## CI fixtures (`fixtures/ci-50.json`)

50 words per locale used by validators and SoundScript tests. Words should appear in `words/common.json` or the corpus pilot list.

## Validation

```bash
python3 scripts/validate.py
```

Validates root manifest, all locale packs, corpus manifest, lemma stubs, and CI fixtures.

# Versioning contract

SoundScript separates **engine releases** from **linguistic data releases**. This document defines how versions align.

## Identifiers

| Layer | Format | Example | Location |
|-------|--------|---------|----------|
| SoundScript engine | `X.Y.Z` semver | `8.0.0` | `sound-script` `Directory.Build.props` |
| Wordbank package | `X.Y.Z` semver | `0.5.0` | `manifest.json` → `version` |
| Corpus snapshot | `YYYY.MM.P` calendar + patch | `2026.07.0` | `corpus/vYYYY.MM/manifest.json` |
| Locale pack | `X.Y.Z` semver | `0.5.0` | `data/<locale>/locale.json` → `version` |

- **Package version** (`manifest.json`) tracks the whole wordbank repo (schemas, locale packs, fixtures).
- **Corpus version** (`corpus/v2026.07/`) tracks large lemma dictionaries independently of engine tables.
- **Patch** `P` on corpus is for data-only fixes within the same monthly snapshot (no schema break).

## Compatibility matrix (v1)

| SoundScript engine | Wordbank package | Corpus | Notes |
|--------------------|------------------|--------|-------|
| `8.0.x` | `>= 0.5.0` | `2026.07.0` | Phase 6–7 pilot corpus |
| `8.0.x` | `>= 0.4.0` | — | Locale packs only (no corpus required) |
| `7.x` | `< 0.4.0` | — | Pre-wordbank integration |

Engines **must not** assume a corpus directory exists. Locale packs under `data/` remain the runtime default.

## Bump rules

1. **Breaking JSON schema** (`schemaVersion` in root manifest): increment `schemaVersion`, bump package minor, document migration.
2. **Locale table change** (phoneme rows, rules): bump locale `version` and package patch/minor.
3. **Corpus lemma add/change**: bump `corpus/vYYYY.MM/manifest.json` patch only.
4. **Engine requirement change**: update `engineCompatibility` in corpus manifest and this table.

## Consumer checks

SoundScript loaders should read:

```json
// corpus/v2026.07/manifest.json
{
  "id": "2026.07",
  "version": 0,
  "engineCompatibility": {
    "soundscriptMin": "8.0.0",
    "wordbankMin": "0.5.0"
  }
}
```

Reject or warn when `wordbankMin` exceeds the loaded package version. Corpus loading is optional until harvest integration lands.

## Release tagging

| Artifact | Git tag | Example |
|----------|---------|---------|
| Wordbank package | `v0.5.0` | GitHub Release zip |
| Corpus snapshot | `corpus-2026.07.0` | Optional additional zip inside release |

Primary install path: **GitHub Release zip** (see [INSTALL.md](INSTALL.md)).

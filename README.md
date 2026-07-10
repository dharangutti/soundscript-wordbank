# SoundScript Wordbank

Deterministic linguistic data for [SoundScript](https://github.com/dharangutti/sound-script) text-to-melody, word-level prosody, syllabification, and offline vocal stems.

**Scope:** A deterministic, offline, multi-language corpus of curated per-word human audio with G2P fallback and DSP transforms, used to generate reproducible vocal stems without relying on eSpeak.

## What's included (v0.6.0)

| Layer | Status | Notes |
|-------|--------|-------|
| Locale packs (`data/`) | v0.6.0 | `en` complete; `es`/`fr` expanded (50+ CI fixture words each) |
| Corpus (`corpus/v2026.07/`) | Pilot | 4 English pronunciations (CC0/CC-BY) + G2P fallback in engine |
| CI fixtures (`fixtures/ci-50.json`) | Active | 50 regression words per locale |

| Locale | Status | Notes |
|--------|--------|-------|
| `en` | Complete | 34-word `common.json` + 1k pilot lemmas |
| `es` | Expanded | 50-word CI fixture coverage in `common.json` |
| `fr` | Expanded | 50-word CI fixture coverage in `common.json` |

Per-locale files:

| File | Purpose |
|------|---------|
| `function-words.json` | Closed-class function words |
| `stress-prefixes.json` | Prefixes that shift stress patterns |
| `word-prosody.json` | Word pitch, phrase contour, stress offsets, clamp bounds |
| `grapheme-rules.json` | Grapheme → phoneme splitting rules |
| `legal-onsets.json` | Legal syllable onsets |
| `phoneme-compose-gestures.json` | Phoneme → musical gesture (compose) |
| `phoneme-wave-frequencies.json` | Phoneme frequency bands (wave speech) |
| `syllabification.json` | Locale-specific syllabification rules (v0.3.0) |
| `phoneme-timbre-profiles.json` | Phoneme → timbre profile table for offline synthesis (v0.3.0) |
| `words/common.json` | Per-word syllable/stress/category overrides |

## Repository layout

```
manifest.json              # top-level package manifest
schema/                    # JSON Schema definitions
data/                      # locale packs (runtime default for SoundScript)
corpus/v2026.07/           # pilot corpus snapshot (see docs/VERSIONING.md)
fixtures/ci-50.json        # CI regression word list
docs/                      # VERSIONING, MANIFEST, INSTALL guides
scripts/
  validate.py              # schema + cross-file validation
  package-release.sh       # build release zip
```

## Validation

```bash
pip install -r scripts/requirements.txt
python scripts/validate.py
```

CI runs the same validator on every push and pull request.

## Data principles

1. **Deterministic** — no random seeds, no locale-sensitive string operations in the data itself.
2. **Rule-first** — heuristics and closed word lists are the default; per-word dictionary entries are optional overrides.
3. **Engine-agnostic JSON** — schemas describe linguistic facts, not C# types. SoundScript loaders map JSON to engine tables.
4. **Locale packs** — `data/<locale>/` holds a self-contained pack; add `data/es/`, `data/fr/`, etc. as languages are supported.

## Runtime loading (SoundScript v0.4+)

SoundScript can load locale packs directly from a wordbank checkout at runtime:

```bash
export WORDBANK_DIR=./wordbank
dotnet run --project src/SoundScript.Cli -- prosody "Hola mundo" out.mid --locale es
# or
dotnet run --project src/SoundScript.Cli -- compose "Bonjour" out.mid --wordbank-dir ./wordbank --locale fr
```

Embedded packs in `SoundScript.Wordbank/Data/` remain the default when no directory is supplied.

## Relationship to SoundScript

This repo is the **data layer**. The main [sound-script](https://github.com/dharangutti/sound-script) repo remains the **engine layer**. Integration (loading wordbank JSON at build time or runtime) is a follow-up phase; v0.1.0 establishes the data format and exports the current built-in English tables.

## License

Data files are released under [CC0 1.0](LICENSE) (public domain dedication). See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## Related documentation

- [SoundScript word-level prosody](https://github.com/dharangutti/sound-script/blob/main/docs/word-prosody.md)
- [SoundScript text-to-melody (phoneme composer)](https://github.com/dharangutti/sound-script/blob/main/docs/text-to-melody.md)
- [SoundScript vocal / syllabification](https://github.com/dharangutti/sound-script/blob/main/docs/vocal.md)

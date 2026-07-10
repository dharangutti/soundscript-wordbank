# SoundScript Wordbank

Deterministic linguistic data for [SoundScript](https://github.com/dharangutti/sound-script) text-to-melody, word-level prosody, syllabification, and synthetic speech engines.

SoundScript's engines are built around a strict determinism guarantee: the same input text must always produce the same output on every platform. Today much of that linguistic knowledge lives as hard-coded tables inside the main repository (`FunctionWords`, `PhonemeMapper`, `Syllabifier`, and others). This repository extracts that data into versioned JSON so it can evolve independently, be reviewed as data, and eventually be consumed at runtime by SoundScript.

## What's included (v0.3.0)

| Locale | Status | Notes |
|--------|--------|-------|
| `en` | Complete | 34-word `common.json` dictionary, full phoneme/prosody/timbre tables |
| `es` | Starter | Spanish function words, grapheme rules, locale syllabification, 10 demo word entries |
| `fr` | Starter | French function words, grapheme rules, nasal digraph syllabification, 10 demo word entries |

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
data/
  en/                      # English locale pack
  es/                      # Spanish locale pack (starter)
  fr/                      # French locale pack (starter)
    locale.json            # locale manifest (file index)
    ...
    words/
      common.json          # per-word overrides
scripts/
  validate.py              # schema + cross-file validation
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

## Relationship to SoundScript

This repo is the **data layer**. The main [sound-script](https://github.com/dharangutti/sound-script) repo remains the **engine layer**. Integration (loading wordbank JSON at build time or runtime) is a follow-up phase; v0.1.0 establishes the data format and exports the current built-in English tables.

## License

Data files are released under [CC0 1.0](LICENSE) (public domain dedication). See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## Related documentation

- [SoundScript word-level prosody](https://github.com/dharangutti/sound-script/blob/main/docs/word-prosody.md)
- [SoundScript text-to-melody (phoneme composer)](https://github.com/dharangutti/sound-script/blob/main/docs/text-to-melody.md)
- [SoundScript vocal / syllabification](https://github.com/dharangutti/sound-script/blob/main/docs/vocal.md)

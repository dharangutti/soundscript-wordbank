# SoundScript Wordbank

Deterministic linguistic data for [SoundScript](https://github.com/dharangutti/sound-script) text-to-melody, word-level prosody, syllabification, and synthetic speech engines.

SoundScript's engines are built around a strict determinism guarantee: the same input text must always produce the same output on every platform. Today much of that linguistic knowledge lives as hard-coded tables inside the main repository (`FunctionWords`, `PhonemeMapper`, `Syllabifier`, and others). This repository extracts that data into versioned JSON so it can evolve independently, be reviewed as data, and eventually be consumed at runtime by SoundScript.

## What's included (v0.1.0)

| File | Purpose | SoundScript source |
|------|---------|-------------------|
| `function-words.json` | Closed-class English function words | `SoundScript.Prosody.FunctionWords` |
| `stress-prefixes.json` | Unstressed two-syllable prefixes | `SoundScript.Prosody.StressDetector` |
| `word-prosody.json` | Word pitch, phrase contour, stress offsets, clamp bounds | `WordPitchTable`, `PhraseContourEngine`, `SyllableContourGenerator`, `ProsodyClamp` |
| `grapheme-rules.json` | Grapheme → phoneme splitting rules | `PhonemeSplitter`, `GraphemePhonemeSplitter` |
| `legal-onsets.json` | Legal English syllable onsets | `Syllabifier` |
| `phoneme-compose-gestures.json` | Phoneme → musical gesture (V3.1 compose) | `PhonemeMapper` |
| `phoneme-wave-frequencies.json` | Phoneme frequency bands (V7 wave speech) | `PhonemeFrequencyTable` |
| `words/seed.json` | Optional per-word overrides (syllables, stress) | Future dictionary expansion |

## Repository layout

```
manifest.json              # top-level package manifest
schema/                    # JSON Schema definitions
data/
  en/                      # English locale pack
    locale.json            # locale manifest (file index)
    function-words.json
    stress-prefixes.json
    word-prosody.json
    grapheme-rules.json
    legal-onsets.json
    phoneme-compose-gestures.json
    phoneme-wave-frequencies.json
    words/
      seed.json            # example word-entry overrides
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

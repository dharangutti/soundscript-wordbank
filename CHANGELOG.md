# Changelog

All notable changes to this repository are documented here.

## [0.6.2] - 2026-07-10

### Added

- **34** new English corpus pronunciations for the full **Jingle Bells** word set (`corpus/v2026.07/audio/en/`, up from 32 to **66**)
- Lingua Libre CC0 recordings for closed-class/function words (`a`, `all`, `and`, `in`, `is`, `on`, `over`, `the`, `to`, `we`) plus song vocabulary (`bells`, `bright`, `fields`, `fun`, `go`, `horse`, `laughing`, `making`, `oh`, `one`, `open`, `ride`, `ring`, `sing`, `sleigh`, `snow`, `song`, `spirits`, `through`, `tonight`, `what`)
- Pilot placeholder clips for `dashing`, `sleighing`, `bobtail` (no standalone CC0/CC-BY Commons clip found; synthesized offline pending harvest, same pattern as `test`/`world`)

### Changed

- `en/lemmas.json` v3 — CI fixture coverage: 27/50 words now have human audio
- `harvest_commons_en.py` — `HARVEST_MANIFEST` extended with Lingua Libre (`LL-Q1860 (eng)-*.wav`) sources; `strip_html()` now collapses multi-line Commons attribution lists into a single readable string

## [0.6.1] - 2026-07-10

### Added

- **32** English corpus pronunciations under `corpus/v2026.07/audio/en/` (up from 4)
- `scripts/harvest_commons_en.py` — Wikimedia Commons harvester (CC0 / CC-BY only, rejects CC-BY-SA)

### Changed

- `en/lemmas.json` v2 — CI fixture coverage: 22/50 words now have human audio
- `welcome` switched to `En-uk-welcome.ogg` (US file was CC-BY-SA)

## [0.6.0] - 2026-07-10

### Added

- Corpus pronunciation audio: `corpus/v2026.07/audio/en/` (hello, welcome, test, world)
- Lemma schema fields: `audio`, `trimStartMs`, `trimEndMs`, `gain`, `pitchSemitones`, `attribution`
- English pilot harvest: 4 CC0/CC-BY entries in `en/lemmas.json`

### Changed

- Validator checks corpus audio file paths and trim bounds
- Package version bumped to v0.6.0

## [0.5.0] - 2026-07-10

### Added

- Corpus pilot layout: `corpus/v2026.07/` with manifest, lemma stubs, and English `pilot-1k.txt` (1000 lemmas)
- CI fixtures: `fixtures/ci-50.json` (50 words per locale)
- Governance docs: `docs/VERSIONING.md`, `docs/MANIFEST.md`, `docs/INSTALL.md`, `LICENSE-POLICY.md`
- Schemas: `corpus-manifest`, `lemmas`, `ci-fixtures`
- `scripts/curate_pilot_1k.py`, `scripts/package-release.sh`
- GitHub Actions release workflow (zip on tag)

### Changed

- Expanded `es`/`fr` `words/common.json` to 50+ entries (CI fixture coverage)
- Validator checks corpus, pilot size, and fixture overlap
- Package version bumped to v0.5.0

## [0.4.0] - 2026-07-10

### Added

- Expanded Spanish `words/common.json` to 34 entries (from 10 demo words)
- Expanded French `words/common.json` to 34 entries (from 10 demo words)

### Changed

- All locale packs bumped to v0.4.0
- `es` and `fr` status upgraded from starter to expanded locale packs

## [0.3.0] - 2026-07-10

### Added

- `syllabification.json` per locale — vowel sets, accented vowels, nucleus digraphs (French), silent-e and consonant-le toggles
- `phoneme-timbre-profiles.json` per locale — exported built-in timbre table from `SoundScript.Timbre`
- JSON Schema definitions for syllabification and phoneme-timbre data files
- Validator checks timbre phoneme parity with compose gesture table

### Changed

- All locale packs bumped to v0.3.0 with new file references in `locale.json`

## [0.2.0] - 2026-07-10

### Added

- Expanded English dictionary: `data/en/words/common.json` (34 word overrides, replaces `seed.json`)
- Spanish (`es`) locale pack — function words, grapheme rules, stress prefixes, demo word entries
- French (`fr`) locale pack — function words, grapheme rules, stress prefixes, demo word entries
- Validator now discovers and validates all locales from `manifest.json`

### Changed

- English locale version bumped to 0.2.0
- Function-word and stress-prefix schemas accept accented characters

## [0.1.0] - 2026-07-10

### Added

- Initial English (`en`) locale pack exported from SoundScript built-in tables
- JSON Schema definitions for all data files
- `scripts/validate.py` with schema validation and cross-file consistency checks
- GitHub Actions `Validate` workflow
- Repository documentation (`README.md`, `CONTRIBUTING.md`)

### Data sources

Exported from [sound-script](https://github.com/dharangutti/sound-script) at initial repo creation:

- `SoundScript.Prosody` — function words, stress prefixes, word pitch, phrase contours
- `SoundScript.Compose` — phoneme gestures and grapheme rules
- `SoundScript.Core.Phonetics` — legal syllable onsets
- `SoundScript.Wave.Prosody` — phoneme frequency table

[0.5.0]: https://github.com/dharangutti/soundscript-wordbank/releases/tag/v0.5.0
[0.4.0]: https://github.com/dharangutti/soundscript-wordbank/releases/tag/v0.4.0
[0.3.0]: https://github.com/dharangutti/soundscript-wordbank/releases/tag/v0.3.0
[0.2.0]: https://github.com/dharangutti/soundscript-wordbank/releases/tag/v0.2.0
[0.1.0]: https://github.com/dharangutti/soundscript-wordbank/releases/tag/v0.1.0

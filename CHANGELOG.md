# Changelog

All notable changes to this repository are documented here.

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

[0.3.0]: https://github.com/dharangutti/soundscript-wordbank/releases/tag/v0.3.0
[0.2.0]: https://github.com/dharangutti/soundscript-wordbank/releases/tag/v0.2.0
[0.1.0]: https://github.com/dharangutti/soundscript-wordbank/releases/tag/v0.1.0

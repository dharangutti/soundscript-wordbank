# Changelog

All notable changes to this repository are documented here.

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

[0.1.0]: https://github.com/dharangutti/soundscript-wordbank/releases/tag/v0.1.0

# License policy (v1)

SoundScript wordbank data must be freely reusable for synthesis, redistribution, and commercial use.

## Allowed licenses

| License | Use in v1 | Notes |
|---------|-----------|-------|
| **CC0 1.0** | Yes (default) | All repo-authored tables and curated overrides |
| **CC-BY 4.0** | Yes (imports only) | External lemma sources; attribution required in `corpus/*/SOURCES.md` |
| **CC-BY-SA** | No | Share-alike incompatible with mixed corpus |
| **All Rights Reserved** | No | |
| **GPL / AGPL** | No | |

## Contribution rule

By contributing to this repository you dedicate changes under **CC0 1.0** (see [CONTRIBUTING.md](CONTRIBUTING.md)).

## Importing CC-BY data

When adding harvested or external lemmas:

1. Record source URL, license, and attribution string in `corpus/vYYYY.MM/<locale>/SOURCES.md`.
2. Do not mix CC-BY text into CC0 files without a clear `license` field per entry (future schema).
3. Run `python3 scripts/validate.py` — pilot lists must be lowercase ASCII/Unicode lemmas only.

## Engine code

C# engine code lives in [sound-script](https://github.com/dharangutti/sound-script) under its own license. This policy applies to **data files only**.

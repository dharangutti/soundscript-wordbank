# Contributing to SoundScript Wordbank

Thank you for helping improve SoundScript's linguistic data.

## What belongs here

- Closed word lists (function words, prefixes)
- Prosody tuning tables (pitch offsets, phrase contours)
- Grapheme-to-phoneme rules
- Phoneme symbol tables for compose / wave engines
- Optional per-word dictionary entries (syllables, stress overrides)

## What does not belong here

- C# engine code (belongs in [sound-script](https://github.com/dharangutti/sound-script))
- SoundCSS timbre styling (`.ssc` files stay in sound-script examples)
- Non-deterministic or model-generated pronunciation data without a reproducible source

## Making changes

1. Edit the relevant JSON file under `data/<locale>/`.
2. Update JSON Schema in `schema/` if you add fields or change structure.
3. Bump `version` in the changed locale file and/or root `manifest.json` for meaningful releases.
4. Run validation locally:

   ```bash
   pip install -r scripts/requirements.txt
   python scripts/validate.py
   ```

5. Open a pull request describing **what linguistic behavior changes** and **why**.

## Word entry guidelines

Per-word entries in `words/*.json` should:

- Use lowercase `word` keys
- Provide `syllables` and `stress` arrays of equal length when both are present
- Only override heuristic output when the rule-based engine is clearly wrong
- Avoid duplicating entries already implied by function-word lists or stress-prefix rules

## Schema changes

Schema changes are breaking when they remove required fields or change enum values. Increment `schemaVersion` in `manifest.json` for breaking schema changes.

## Licensing

By contributing data, you agree that your contributions are dedicated to the public domain under [CC0 1.0](LICENSE), consistent with the project's goal of freely reusable linguistic tables.

# Corpus v2026.07 (pilot)

July 2026 pilot snapshot for large-scale lemma dictionaries.

## Layout

```
corpus/v2026.07/
  manifest.json       # corpus manifest (see docs/MANIFEST.md)
  en/
    pilot-1k.txt      # 1000 curated lemmas (one per line, Phase 7)
    lemmas.json       # harvested entries (empty at pilot start)
    SOURCES.md        # attribution for CC-BY imports
  es/
    lemmas.json       # stub — pilot list deferred to v2026.08
  fr/
    lemmas.json       # stub — pilot list deferred to v2026.08
```

## Status

| Locale | Pilot list | Lemma harvest |
|--------|------------|---------------|
| `en` | 1000 lemmas (`pilot-1k.txt`) | Not started (`entries: []`) |
| `es` | Deferred | Stub only |
| `fr` | Deferred | Stub only |

Locale packs under `data/` remain the runtime source for SoundScript engines. This corpus directory is versioned separately per [VERSIONING.md](../../docs/VERSIONING.md).

## Validation

```bash
python3 scripts/validate.py
```

Checks corpus manifest, lemma stubs, pilot line count, and CI fixture overlap.

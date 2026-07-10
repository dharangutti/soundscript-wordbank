# Installation

## Primary path: GitHub Release zip (recommended)

Tagged releases publish `soundscript-wordbank-vX.Y.Z.zip` containing:

```
manifest.json
schema/
data/
corpus/
fixtures/
LICENSE
```

**Use when:** you want a frozen data snapshot without git submodules.

```bash
curl -L -o wordbank.zip https://github.com/dharangutti/soundscript-wordbank/releases/download/v0.5.0/soundscript-wordbank-v0.5.0.zip
unzip wordbank.zip -d soundscript-wordbank
export WORDBANK_DIR="$PWD/soundscript-wordbank"
```

## Git submodule (SoundScript development)

The `sound-script` repo vendors wordbank at `wordbank/`:

```bash
git clone --recurse-submodules https://github.com/dharangutti/sound-script.git
cd sound-script
./scripts/sync-wordbank.sh
```

Update to latest wordbank `main`:

```bash
./scripts/bump-wordbank-submodule.sh
```

## Runtime directory (SoundScript CLI)

Load any checkout at runtime without rebuilding:

```bash
export WORDBANK_DIR=/path/to/soundscript-wordbank
dotnet run --project src/SoundScript.Cli -- prosody "Hello" out.mid --locale en
# or
dotnet run --project src/SoundScript.Cli -- compose "Hola" out.mid --wordbank-dir "$WORDBANK_DIR" --locale es
```

## NuGet (not v1)

A `SoundScript.Wordbank.Data` NuGet package is **deferred**. JSON linguistic tables change frequently; zip + submodule keep review and diffing simpler for v1.

Revisit NuGet when:

- corpus harvest produces stable monthly snapshots, and
- consumers need MSBuild embedding without a submodule.

## Decision record

| Path | v1 status | Rationale |
|------|-----------|-----------|
| GitHub Release zip | **Primary** | Language-agnostic, easy audit, matches corpus calendar releases |
| Git submodule | **Developer default** | Tight coupling for SoundScript CI |
| `WORDBANK_DIR` / `--wordbank-dir` | **Supported** | Local iteration and custom packs |
| NuGet | **Deferred** | Adds packaging overhead before corpus scale is stable |

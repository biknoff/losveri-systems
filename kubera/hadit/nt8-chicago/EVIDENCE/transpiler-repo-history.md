# Evidence: the transpiler as surviving descendant

**What this is:** the directory structure of `NinjaScript.Transpiler/`, the one piece of
the Chicago-era bridge tooling that still exists as a standalone artifact, plus what its
containing repo's history says about it.

**Redactions applied:** no trading-strategy source was read or reproduced. The excerpt in
`SNIPPETS/` is pure classification/parsing code with no strategy rules in it.

## Structure

```
NinjaScript.Transpiler/
├── .claude/
├── input/
│   ├── AddOns/
│   ├── Indicators/
│   ├── Strategies/
│   └── Unsupported/
├── output/
├── outputcd
├── Program.cs         (372 lines)
└── <project>.csproj
```

This is a Roslyn-based C# source classifier/cataloger: it parses NinjaScript `.cs` files
(Strategies / Indicators / AddOns, distinguished by base-type) into a catalog model
(`StrategyCatalog`, `StrategyFileInfo`, `ParameterInfo`). It is a static-analysis tool over
NinjaScript source — not a runtime bridge that executes inside NT8. See
`SNIPPETS/transpiler-classifier.cs` for a verbatim, non-strategy excerpt showing the
classification mechanism.

## What the containing repo's git history shows

The transpiler used to live inside a larger monorepo alongside other components. That
monorepo's history now shows only its *removal*: the top commit on the relevant path,
dated Friday 2026‑05‑29, reads (paraphrased structurally, exact message is generic and
non-sensitive):

> chore: untrack `ninjascript-transpiler` (extracted to standalone Hadit-Nautilus repo)

A path-scoped `git log` against `NinjaScript.Transpiler/` inside that monorepo returns no
commits at all — the code was never tracked at that path in that repo's history; it was
developed elsewhere and only its extraction/removal is recorded here. The live,
developed copy is the one preserved on the build host (`hadit-nautilus/`), which is the
source used for the counts and excerpt in this project directory.

**Interpretation:** the transpiler's own repo lineage is itself a small piece of evidence
for the "we evolved out of consumer-grade NT8/Windows" narrative — at the point the team
moved off the Chicago pipeline, the transpiler was deliberately extracted and kept as a
standalone tool rather than deleted, while the rest of the monorepo's Chicago-era content
was left behind.

**Source commands (read-only):** directory listing of `NinjaScript.Transpiler/` on the
build host; `git log` (unscoped and path-scoped) inside the mirror-host copy of its
containing repo.

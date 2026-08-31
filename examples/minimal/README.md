# Minimal package example

This directory is the only place in the schema repository containing concrete rule instances.

- `definitions.pkl` demonstrates a terminology package.
- `ruleset.pkl` demonstrates a concrete package that references that terminology.
- `axioval.json` is the static manifest a registry can inspect without evaluating Pkl.

Evaluate the normalized representations:

```bash
pkl eval -f json definitions.pkl
pkl eval -f json ruleset.pkl
```

The example is deliberately non-production. Real official and community packages live in independent repositories and use the same manifest and schema contract.

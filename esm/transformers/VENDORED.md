# Vendored ESM-C / ESMFold2 modeling code

Everything under `models/` is copied **verbatim** from the patched transformers fork.
Do not edit those files — edits are silently reverted on the next re-sync.

| | |
| --- | --- |
| Source | `https://github.com/Biohub/transformers.git` |
| Path | `src/transformers/models/{esmc,esmfold2}` |
| Pinned commit | `ef32577f55da19a4989cd7b22e004dc43a4998cb` |
| Upstream base | `753d611041` (transformers v4.57.6) |
| Size | 30 files, ~14,251 lines |

## Why the layout mirrors `transformers/`

The vendored code uses relative imports that reach the transformers package root:

```python
from ...modeling_utils import PreTrainedModel      # 4 occurrences
from ...utils import logging, auto_docstring, ...  # 7
from ...configuration_utils import PretrainedConfig # 3
from ...modeling_outputs import ...                 # 2
from ...tokenization_utils_fast import ...          # 1
```

Living at `esm.transformers.models.<model>`, those three dots resolve to
`esm.transformers` — so the shim modules in this package (`modeling_utils.py`,
`configuration_utils.py`, `modeling_outputs.py`, `tokenization_utils_fast.py`,
`utils/`) satisfy all 17 of them by re-exporting from the real installed
`transformers`.

**This is why no rewriting is needed and the tree stays byte-identical to upstream.**
Two consequences worth preserving:

- `diff -r` against a fresh upstream checkout shows only genuine upstream changes.
- Re-syncing is a plain copy, with no post-processing step to get wrong.

Do **not** flatten `models/esmc` to `esmc`: `...` would then resolve to `esm` and
every vendored module would break.

`models/esmc` and `models/esmfold2` must also stay siblings — `modeling_esmfold2.py`
and `modeling_esmfold2_experimental.py` both do `from ..esmc.modeling_esmc import
ESMCModel`.

`models/esmfold2/kernels/` and `models/esmfold2/distributed/` (~5,750 lines) contain
no transformers imports at all and port unchanged.

## Re-syncing

```bash
tools/sync_hf_modeling.sh                    # re-fetch the pinned commit
tools/sync_hf_modeling.sh <new-sha>          # bump to a new upstream commit
git diff esm/transformers/models             # review the pure upstream delta
```

Commit the SHA bump as its own change so it can be reverted independently.

## Relationship to the native `esm` code

This package is **not** the SDK-facing surface:

- `esm/models/esmc.py` — native `ESMC`, unrelated to the vendored `ESMCModel`.
- `esm/models/esmfold2/` — the data plane (input building, MSA features, ligands,
  output parsing). The vendored `models/esmfold2/protein_utils.py` is a much smaller
  single-protein path (`prepare_protein_features`, `output_to_pdb`) that duplicates a
  fraction of it. Converging the two is deliberately left as a separate change.

## When transformers#46419 lands

[PR #46419](https://github.com/huggingface/transformers/pull/46419) upstreams ESM-C and
ESMFold2 into HuggingFace transformers. When it ships, most of this directory can be
deleted and replaced with re-exports from `transformers.models.{esmc,esmfold2}`.

Three things will not survive that move and stay vendored permanently — the port drops
or defers them:

- `models/esmfold2/kernels/` (Triton) — upstream uses `integrations/hub_kernels.py`
- `models/esmfold2/distributed/` (tensor parallel) — dropped
- `modeling_esmfold2_experimental.py` (looped) and `modeling_esmc_sae.py` — deferred,
  no follow-up PR filed as of 2026-07-27

Expect config changes too: the port flattens the config (no subconfigs) and moves
weight renames into a conversion script, so checkpoints need re-conversion.

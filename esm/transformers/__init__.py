"""Transformers-derived ESM models, vendored verbatim from the patched fork.

This package deliberately mirrors the layout of the upstream ``transformers``
package root. Vendored model code under ``models/`` uses relative imports of the
form ``from ...modeling_utils import PreTrainedModel``; because that code lives at
``esm.transformers.models.<model>``, those three dots resolve to
``esm.transformers`` — i.e. to the thin re-export shims in this package, which
forward to the real installed ``transformers``.

The consequence is that **everything under ``models/`` is byte-identical to
upstream** and needs no rewriting when re-synced. Do not flatten the layout: moving
``models/esmc`` to ``esmc`` would make ``...`` resolve to ``esm`` and break every
vendored module.

Provenance and re-sync instructions live in ``VENDORED.md``; re-sync with
``tools/sync_hf_modeling.sh``.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Cosmetic: teach upstream's `auto_docstring` about the vendored model types.
#
# `auto_docstring` runs at class-definition time and looks the config up in a
# module-level dict, printing "[ERROR] Config not found for esmc" for anything it
# does not know. The dict is the documented extension point (upstream seeds it with
# entries such as "esmfold": "EsmConfig"), and AutoConfig.register does not feed it.
#
# This runs at package-import time, which is before any vendored modeling module can
# be imported, since importing `esm.transformers.models.*` executes this file first.
# Purely a logging fix — guarded so a transformers version that drops the dict is
# still fine.
# ---------------------------------------------------------------------------
try:
    # Must go through importlib: `transformers.utils` re-exports a function named
    # `auto_docstring`, which shadows the submodule of the same name on attribute
    # access. import_module returns the module itself.
    from importlib import import_module as _import_module

    _hardcoded = getattr(
        _import_module("transformers.utils.auto_docstring"),
        "HARDCODED_CONFIG_FOR_MODELS",
        None,
    )
    if _hardcoded is not None:
        _hardcoded.setdefault("esmc", "ESMCConfig")
        _hardcoded.setdefault("esmfold2", "ESMFold2Config")
except Exception:  # pragma: no cover - never let a cosmetic fix break imports
    pass


def register_auto_classes() -> None:
    """Register the vendored models with the transformers ``Auto*`` registries.

    Makes ``AutoConfig``, ``AutoModel`` and ``AutoTokenizer`` resolve the ``esmc``
    and ``esmfold2`` model types, so the vendored models load through the same API
    as any upstream model.

    Safe to call more than once; re-registration errors are ignored.
    """
    from transformers import AutoConfig, AutoModel, AutoTokenizer

    from esm.transformers.models.esmc.configuration_esmc import ESMCConfig
    from esm.transformers.models.esmc.modeling_esmc import ESMCModel
    from esm.transformers.models.esmc.tokenization_esmc import ESMCTokenizer
    from esm.transformers.models.esmfold2.configuration_esmfold2 import ESMFold2Config
    from esm.transformers.models.esmfold2.modeling_esmfold2 import ESMFold2Model

    for name, config_cls, model_cls in (
        ("esmc", ESMCConfig, ESMCModel),
        ("esmfold2", ESMFold2Config, ESMFold2Model),
    ):
        try:
            AutoConfig.register(name, config_cls)
            AutoModel.register(config_cls, model_cls)
        except ValueError:
            pass  # already registered

    try:
        AutoTokenizer.register(ESMCConfig, slow_tokenizer_class=ESMCTokenizer)
    except ValueError:
        pass

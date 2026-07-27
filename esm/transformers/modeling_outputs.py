"""Shim: resolves ``from ...modeling_outputs import ...`` in vendored model code."""

from transformers.modeling_outputs import (  # noqa: F401
    MaskedLMOutput,
    ModelOutput,
    SequenceClassifierOutput,
    TokenClassifierOutput,
)

__all__ = [
    "MaskedLMOutput",
    "ModelOutput",
    "SequenceClassifierOutput",
    "TokenClassifierOutput",
]

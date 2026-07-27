"""Shim: resolves ``from ...tokenization_utils_fast import ...`` in vendored model code."""

from transformers.tokenization_utils_fast import PreTrainedTokenizerFast  # noqa: F401

__all__ = ["PreTrainedTokenizerFast"]

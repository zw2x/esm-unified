"""Shim: resolves ``from ...modeling_utils import ...`` in vendored model code."""

from transformers.modeling_utils import PreTrainedModel  # noqa: F401

__all__ = ["PreTrainedModel"]

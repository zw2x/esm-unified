"""Shim: resolves ``from ...configuration_utils import ...`` in vendored model code."""

from transformers.configuration_utils import PretrainedConfig  # noqa: F401

__all__ = ["PretrainedConfig"]

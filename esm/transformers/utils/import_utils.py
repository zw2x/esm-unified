"""Shim: resolves ``from ...utils.import_utils import ...`` in vendored model code."""

from transformers.utils.import_utils import define_import_structure  # noqa: F401

__all__ = ["define_import_structure"]

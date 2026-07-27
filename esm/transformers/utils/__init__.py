"""Shim: resolves ``from ...utils import ...`` in vendored model code."""

from transformers.utils import (  # noqa: F401
    _LazyModule,
    auto_docstring,
    can_return_tuple,
    is_flash_attn_2_available,
    logging,
)

__all__ = [
    "_LazyModule",
    "auto_docstring",
    "can_return_tuple",
    "is_flash_attn_2_available",
    "logging",
]

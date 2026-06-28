"""Utility helpers for serialising animation parameters.

The frontend animation wrappers (GSAP, Three.js, etc.) often need a JSON
payload that originates from Python data structures. ``json.dumps`` is
sufficient for most cases, but we also provide a thin wrapper that ensures
keys are camelCased to match typical JavaScript conventions.
"""

import json
import re
from typing import Any, Mapping

def _camel_case(s: str) -> str:
    parts = s.split("_")
    return parts[0] + "".join(p.title() for p in parts[1:])

def serialize_params(params: Mapping[str, Any]) -> str:
    """Return a JSON string with keys converted to ``camelCase``.

    Args:
        params: Mapping of parameter names to values.
    Returns:
        JSON string safe to embed in a ``<script>`` tag.
    """
    camelized = { _camel_case(k): v for k, v in params.items() }
    return json.dumps(camelized)

__all__ = ["serialize_params"]

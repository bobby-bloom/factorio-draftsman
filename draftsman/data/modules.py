# modules.py
# -*- encoding: utf-8 -*-

import pickle

try:  # pragma: no coverage
    import importlib.resources as pkg_resources  # type: ignore
except ImportError:  # pragma: no coverage
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources  # type: ignore

from draftsman import data


with pkg_resources.open_binary(data, "modules.pkl") as inp:
    _data = pickle.load(inp)
    raw: dict[str, dict] = _data[0]
    categories: dict[str, list[str]] = _data[1]


def add_module(name: str, category: str):
    raise NotImplementedError

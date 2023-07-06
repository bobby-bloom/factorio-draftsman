# items.py

import pickle

try:  # pragma: no coverage
    import importlib.resources as pkg_resources  # type: ignore
except ImportError:  # pragma: no coverage
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources  # type: ignore

from draftsman import data


with pkg_resources.open_binary(data, "items.pkl") as inp:
    _data = pickle.load(inp)
    raw: dict[str, dict] = _data[0]
    subgroups: dict[str, dict] = _data[1]
    groups: dict[str, dict] = _data[2]


def add_item(name: str, subgroup: str, group: str):
    raise NotImplementedError

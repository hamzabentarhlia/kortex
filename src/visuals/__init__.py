import importlib
import pkgutil
import re

from . import kit

REGISTRY = {}
MODULE_OF = {}

for _m in pkgutil.iter_modules(__path__):
    if _m.name == "kit":
        continue
    try:
        _mod = importlib.import_module(f"{__name__}.{_m.name}")
    except Exception as _e:
        print(f"visual module {_m.name} failed to load: {_e}")
        continue
    for _k, _fn in getattr(_mod, "VISUALS", {}).items():
        REGISTRY[_k] = _fn
        MODULE_OF[_k] = _m.name


def render(name, lang):
    kit.reset(name)
    return f'<div class="vx" data-v="{name}">{REGISTRY[name](lang)}</div>'


def modules_in(body):
    names = set(re.findall(r'data-v="([a-z0-9-]+)"', body))
    return sorted({MODULE_OF.get(n, n) for n in names})

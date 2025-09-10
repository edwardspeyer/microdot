from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import microdot.registry
from microdot.hooks import BASE


def find_module_paths() -> list[Path]:
    """The heuristic is that any .py _not_ alongside an __init__.py is probably
    a small script, and should be ignored."""
    IGNORE = {".venv", ".git"}
    packages = {p.parent for p in BASE.rglob("__init__.py") if not (set(p.parts) & IGNORE)}
    modules = {p for d in packages for p in d.glob("*.py")}
    return sorted(modules)


def main() -> None:
    for path in find_module_paths():
        spec = spec_from_file_location("??", path)
        assert spec is not None
        assert spec.loader is not None
        module = module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except ImportError as exc:
            print(f"Skipping {path} due to {exc!r}")

    for f in microdot.registry.registry:
        f()


if __name__ == "__main__":
    main()

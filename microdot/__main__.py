from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import microdot.registry
from microdot.hooks import BASE


def find_module_paths() -> list[Path]:
    """The heuristic is that any .py _not_ alongside an __init__.py is probably
    a small script, and should be ignored."""
    packages = {p.parent for p in BASE.rglob("__init__.py")}
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


"""
TODO run all these old functions as well

-actions = {
-    "install": (
-        "Run `hooks` and `terminfos`, see below.",
-        install,
-    ),
-    "hooks": (
-        "Install config file hooks.",
-        microdot.hooks.search_and_install,
-    ),
-    "terminfos": (
-        "Install missing terminfo for common TERM settings.",
-        microdot.terminfo.install,
-    ),
-    "debian": (
-        "Install some common debian packages.",
-        microdot.packages.debian.install,
-    ),
-    "python": (
-        "Install some common python packages.",
-        microdot.packages.python.install,
-    ),
-    "delta": (
-        "Install git-delta from source.",
-        microdot.packages.source.delta.install,
-    ),
-    "fish": (
-        "Install a newer version of fish (if required) from source.",
-        microdot.packages.source.fish.install,
-    ),
-    "i3": (
-        "Install a newer version of i3 (if required) from source.",
-        microdot.packages.source.i3.install,
-    ),
-    "tmux": (
-        "Install a new version of tmux (if required) from source.",
-        microdot.packages.source.tmux.install,
-    ),
-    "gpg": (
-        "Install my GPG key stubs, for use with yubikeys.",
-        microdot.gnupg.install,
-    ),
-    "fonts": (
-        "Download and install some extra fonts.",
-        microdot.fonts.install,
-    ),
-    "macos": (
-        "Configure a macOS user account.",
-        microdot.macos.setup,
-    ),
-}
"""

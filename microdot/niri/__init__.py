from microdot import cwd, install_hook

from .build import build

__all__ = ["build"]


def configure() -> None:
    install_hook("~/.config/niri/config.kdl", f'include "{cwd()}/config.kdl"', position="top", comment="//")

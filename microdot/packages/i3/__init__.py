from microdot import cwd, install_hook

from . import build

__all__ = ["build"]


def configure() -> None:
    install_hook(
        "~/.config/i3/config",
        f"""\
        include {cwd()}/config
        """,
    )

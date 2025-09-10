from microdot import cwd, install_hook

from . import build

__all__ = ["build"]


def configure() -> None:
    install_hook(
        "~/.tmux.conf",
        f"""\
        source {cwd()}/tmux.conf
        """,
    )

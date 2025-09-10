from microdot import cwd, install_hook
from microdot.terminfo import install_terminfo

from .build import build

__all__ = ["build"]


def configure() -> None:
    install_hook(
        "~/.tmux.conf",
        f"""\
        source {cwd()}/tmux.conf
        """,
    )

    for p in (cwd() / "terminfo").glob("*"):
        install_terminfo(p)

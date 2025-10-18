from microdot import cwd, install_hook

from .build import build

__all__ = ["build"]


def configure():
    install_hook(
        "~/.config/fish/conf.d/microdot.fish",
        f"""\
        for file in {cwd()}/*.fish
            source $file
        end
        """,
    )

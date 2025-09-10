from microdot import cwd, install_hook
from microdot.terminfo import install_terminfo


def configure() -> None:
    install_hook(
        "~/.config/kitty/kitty.conf",
        f"""\
        include {cwd()}/kitty.conf
        """,
    )

    install_terminfo(cwd() / "terminfo" / "kitty")

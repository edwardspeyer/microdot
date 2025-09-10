from microdot import cwd, install_hook
from microdot.terminfo import install_terminfo


def configure() -> None:
    install_hook(
        "~/.config/foot/foot.ini",
        f"""\
        include={cwd()}/foot.ini
        """,
    )

    install_terminfo(cwd() / "terminfo" / "foot")

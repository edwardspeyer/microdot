from microdot import install_hook
from microdot.xkb.xcompose import build_xcompose


def configure() -> None:
    path = build_xcompose()
    install_hook(
        "~/.XCompose",
        f"""\
        include "{path}"
        """,
    )

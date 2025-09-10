from microdot import cwd, install_hook


def configure() -> None:
    install_hook(
        "~/.config/kitty/kitty.conf",
        f"""\
        include {cwd()}/kitty.conf
        """,
    )

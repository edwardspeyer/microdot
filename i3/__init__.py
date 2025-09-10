from microdot import cwd, install_hook


def configure() -> None:
    install_hook(
        "~/.config/i3/config",
        f"""\
        include {cwd()}/config
        """,
    )

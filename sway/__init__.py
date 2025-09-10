from microdot import cwd, install_hook


def configure() -> None:
    install_hook(
        "~/.config/sway/config",
        f"""\
        include {cwd()}/config
        """,
    )

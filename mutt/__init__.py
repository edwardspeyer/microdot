from microdot import cwd, install_hook


def configure() -> None:
    install_hook(
        "~/.muttrc",
        f"""\
        source {cwd()}/muttrc
        """,
        position="bottom",
    )

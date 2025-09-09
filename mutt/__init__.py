from microdot import cwd, install_hook, register


@register
def configure() -> None:
    install_hook(
        "~/.muttrc",
        f"""\
        source {cwd()}/muttrc
        """,
        position="bottom",
    )

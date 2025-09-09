from microdot import cwd, install_hook, register


@register
def configure() -> None:
    install_hook(
        "~/.config/i3/config",
        f"""\
        include {cwd()}/config
        """,
    )

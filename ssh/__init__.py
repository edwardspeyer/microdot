from microdot import cwd, install_hook, register


@register
def configure() -> None:
    install_hook(
        "~/.ssh/config",
        f"""\
        Host *
        Include {cwd()}/config
        """,
        position="bottom",
    )

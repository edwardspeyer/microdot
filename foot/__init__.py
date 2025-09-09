from microdot import cwd, install_hook, register


@register
def configure() -> None:
    install_hook(
        "~/.config/foot/foot.ini",
        f"""\
        include={cwd()}/foot.ini
        """,
    )

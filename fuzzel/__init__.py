from microdot import cwd, install_hook, register


@register
def configure() -> None:
    install_hook(
        "~/.config/fuzzel/fuzzel.ini",
        f"""\
        [main]
        include = {cwd()}/fuzzel.ini
        """,
    )

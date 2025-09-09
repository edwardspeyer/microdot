from microdot import cwd, install_hook, register


@register
def configure() -> None:
    install_hook(
        "~/.gitconfig",
        f"""\
        [include]
        path = {cwd()}/config

        [core]
        excludesfile = {cwd()}/ignore
        """,
    )

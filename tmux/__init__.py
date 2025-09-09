from microdot import cwd, install_hook, register


@register
def configure() -> None:
    install_hook(
        "~/.tmux.conf",
        f"""\
        source {cwd()}/tmux.conf
        """,
    )

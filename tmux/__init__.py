from microdot import cwd, install_hook


def configure() -> None:
    install_hook(
        "~/.tmux.conf",
        f"""\
        source {cwd()}/tmux.conf
        """,
    )

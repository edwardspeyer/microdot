from microdot import cwd, install_hook


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

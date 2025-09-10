from microdot import cwd, install_hook


def configure() -> None:
    install_hook(
        "~/.xsession",
        f"""\
        # Hand control to microdot's xsession
        exec {cwd()}/xsession
        """,
        position="bottom",
        mode=0o744,
    )

    install_hook(
        "~/.XCompose",
        f"""\
        include "{cwd()}/XCompose"
        """,
    )

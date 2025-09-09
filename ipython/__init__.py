from microdot import cwd, install_hook, register


@register
def configure() -> None:
    install_hook(
        "~/.config/ipython/profile_default/startup/microdot.py",
        f"""\
        exec(open("{cwd()}/config.py").read())
        """,
    )

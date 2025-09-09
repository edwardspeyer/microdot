from microdot import cwd, install_hook, register


@register
def configure():
    install_hook(
        "~/.config/apt.conf",
        f"""\
        // Requires APT_CONFIG to also be set in the environment
        #include "{cwd()}/apt.conf";
        """,
        comment="//",
    )

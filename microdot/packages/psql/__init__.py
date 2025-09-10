from microdot import cwd, install_hook


def configure() -> None:
    install_hook(
        "~/.config/psqlrc",
        rf"\i {cwd()}/psqlrc",
        comment="--",
    )

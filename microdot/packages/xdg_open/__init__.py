from microdot import cwd, install_hook


def configure():
    install_hook(
        "~/.config/mimeapps.list",
        (cwd() / "mimeapps.list").read_text(),
        position="bottom",
    )

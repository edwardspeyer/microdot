from microdot import cwd, install_hook, register


@register
def configure():
    install_hook(
        "~/.config/mimeapps.list",
        (cwd() / "mimeapps.list").read_text(),
        position="bottom",
    )

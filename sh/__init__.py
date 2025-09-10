from pathlib import Path

from microdot import BASE, install_hook


def configure() -> None:
    # These config files should all hook into the generic sh startup code.
    for rc in [".profile", ".bashrc", ".zshrc"]:
        install_hook(
            Path.home() / rc,
            f"""\
            export MICRODOT_INSTALL_PATH="{BASE}"
            . $MICRODOT_INSTALL_PATH/sh/profile
            """,
        )

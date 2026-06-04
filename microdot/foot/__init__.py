import os
import sys
from configparser import ConfigParser as Config
from pathlib import Path
from subprocess import check_output

from microdot import cwd, install_hook
from microdot.terminfo import install_terminfo

COLORS = {
    "background": "000000",
    "regular0": "000000",  # black
    "regular3": "cecb00",  # yellow
    "regular4": "1a8fff",  # blue
}


def configure() -> None:
    install_hook(
        "~/.config/foot/foot.ini",
        f"""\
        include={cwd()}/foot.ini
        """,
    )

    install_terminfo(cwd() / "terminfo" / "foot")


def start() -> None:
    """Foot 1.26 changed the [colors] section to [colors-dark], made the old
    setting deprecated, and doesn't provide a way to suppress the deprecated
    messages.

    Regular Debian is on 1.21 and sid is on 1.27.  This function builds a
    wrapper config that (a) sets mY faVouriTe cOLorS; (b) hooks back into
    ~/.config/foot/foot.ini; and (c) execs into foot.
    """

    def get_foot_version() -> list[int]:
        output = check_output(["foot", "--version"], text=True)
        fields = output.split()
        assert fields[1] == "version:"
        return [int(v) for v in fields[2].split(".")]

    def build_config() -> Config:
        config = Config()
        config["main"] = {"include": "~/.config/foot/foot.ini"}
        if get_foot_version() >= [1, 26]:
            config["main"]["initial-color-theme"] = "dark"
            config["colors-dark"] = COLORS
        else:
            config["colors"] = COLORS
        return config

    tmp_config = Path.home() / ".config" / "foot" / ".microdot_foot.ini"
    with tmp_config.open("wt") as f:
        build_config().write(f)
    argv = ("foot", "--config", str(tmp_config), *sys.argv[1:])
    os.execvp("foot", argv)

"""Automate a few post-install things."""

import shlex
from getpass import getuser
from pathlib import Path
from subprocess import DEVNULL, run
from textwrap import dedent
from typing import Iterable

from microdot.paths import BASE


def setup_sudo():
    def is_configured() -> bool:
        return run("which sudo && sudo -n id", shell=True).returncode == 0

    if is_configured():
        return

    user = getuser()
    script = dedent(
        """\
        set -ex
        user=$1
        apt install --yes sudo
        echo "$user ALL=(ALL:ALL) NOPASSWD:ALL" > /etc/sudoers.d/$user
        """
    )
    command = shlex.join(["sh", "-c", script, "--", user])
    run(["su", "-c", command])
    assert is_configured()


def write(path: Path, text: str) -> bool:
    if path.exists() and path.read_text() == text:
        return False
    script = "mkdir -p $1 && tee $2"
    command = ["sh", "-c", script, "--", str(path.parent), str(path)]
    run(["sudo", *command], check=True, input=text, text=True, stdout=DEVNULL)
    return True


def setup_locales(expected: Iterable[str]) -> None:
    path = Path("/etc/locale.gen")
    config = "".join(f"{v}\n" for v in sorted(expected))
    if path.read_text() == config:
        return
    if write(path, config):
        run(["sudo", "locale-gen"], check=True)


def setup_timezone(tz_name: str) -> None:
    path = Path("/etc/timezone")
    if path.exists() and path.read_text().strip() == tz_name:
        return
    write(path, f"{tz_name}\n")


def setup_console() -> None:
    path = Path("/etc/default/console-setup")
    config = dedent(
        """\
        ACTIVE_CONSOLES="/dev/tty[1-6]"
        CHARMAP="UTF-8"
        CODESET="Lat15"
        FONTFACE="TerminusBold"
        FONTSIZE="16x32"
        """
    )
    if write(path, config):
        run("sudo service console-setup restart", shell=True)


def setup_greetd() -> None:
    user = getuser()
    path = Path("/etc/greetd/config.toml")
    config = dedent(
        f"""\
        [terminal]
        vt = 7

        [default_session]
        command = "{BASE}/greetd/init"
        user = "{user}"
        """
    )
    write(path, config)


def setup():
    setup_sudo()
    setup_locales({"en_GB.UTF-8 UTF-8", "en_US.UTF-8 UTF-8"})
    setup_timezone("Etc/UTC")
    setup_console()
    setup_greetd()


if __name__ == "__main__":
    setup()

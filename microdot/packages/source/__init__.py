import os
import platform
from pathlib import Path
from shutil import copytree
from subprocess import run
from tempfile import TemporaryDirectory

FISH_VERSION = "3.6.0"
I3_VERSION = "4.22"
TMUX_VERSION = "3.3a"
DELTA_VERSION = "0.15.1"


def install():
    if not is_linux():
        return
    install_delta()
    install_fish()
    install_i3()
    install_tmux()


def install_delta():
    if DELTA_VERSION in shell_output("delta --version"):
        return
    script_install("delta", DELTA_VERSION)


def install_fish():
    if FISH_VERSION in shell_output("fish --version"):
        return
    script_install("fish", FISH_VERSION)


def install_i3():
    if I3_VERSION in shell_output("i3 --version"):
        return
    script_install("i3", I3_VERSION)


def install_tmux():
    if TMUX_VERSION in shell_output("tmux -V"):
        return
    script_install("tmux", TMUX_VERSION)


def shell_output(script):
    return run(
        script,
        capture_output=True,
        check=False,
        shell=True,
        text=True,
    ).stdout.strip()


def script_install(name, *args):
    with TemporaryDirectory() as temporary_directory:
        tmp = Path(temporary_directory)
        base = Path(__file__).parent
        script = base / f"{name}.sh"
        env = dict(os.environ)
        env["DEBIAN_FRONTEND"] = "noninteractive"
        env["PATH"] = f"/usr/lib/ccache:{env['PATH']}"
        run(["sh", script, *args], check=True, cwd=tmp, env=env)
        out = tmp / "out"
        local = Path.home() / ".local"
        copytree(out, local, dirs_exist_ok=True)


def is_linux():
    return platform.system() == "Linux"

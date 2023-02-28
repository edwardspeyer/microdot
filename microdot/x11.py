from pathlib import Path
from shutil import copy
from subprocess import run

# TODO install x11-xserver-utils, kitty, firefox etc.?


def install():
    base = Path(__file__).parent.parent
    source = base / "X11" / "system"

    xsessions_directory = Path("/usr/share/xsessions")
    if xsessions_directory.exists():
        copy(source / "xsession.desktop", xsessions_directory)

    xorg_conf_directory = Path("/etc/X11/xorg.conf.d")
    if xorg_conf_directory.exists() and has_amd_gpu():
        copy(source / "20-xorg-amdgpu.conf", xorg_conf_directory)


def has_amd_gpu():
    process = run("lspci", capture_output=True, text=True, shell=True)
    for line in process.stdout.splitlines():
        if "AMD" in line and "Graphics" in line:
            return True
    return False


if __name__ == "__main__":
    install()

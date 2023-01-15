"""Install from source on hosts where all we have for certain is Docker"""

import platform
from pathlib import Path
from subprocess import run

FISH_VERSION = "3.6.0"
TMUX_VERSION = "3.3a"
DELTA_VERSION = "0.15.1"


def shell(script):
    return run(
        script,
        capture_output=True,
        check=False,
        shell=True,
        text=True,
    ).stdout.strip()


def is_linux():
    return platform.system() == "Linux"


def is_docker_installed():
    return shell("which docker") != ""


def install_delta():
    if DELTA_VERSION in shell("delta --version"):
        return
    docker_install("delta", DELTA_VERSION)


def install_fish():
    if FISH_VERSION in shell("fish --version"):
        return
    docker_install("fish", FISH_VERSION)


def install_tmux():
    if TMUX_VERSION in shell("tmux -V"):
        return
    docker_install("tmux", TMUX_VERSION)


def docker_install(name, version):
    """Install stuff via a Dockerfile

    For the package named `name` we assume (1) there is a path alongside this
    module called `<name>/Dockerfile`; which (2) builds everything it needs
    into /out.

    We build that image then copy everything we find in /out into ~/.local.
    """
    image_name = f"microdot-{name}"
    base = Path(__file__).parent / name
    container_name = f"microdot-{name}"
    run(
        f"""
        set -ex
        docker build --tag {image_name} --build-arg VERSION={version} .
        docker run --name {container_name} --rm {image_name} \
            tar -C /out -cf - .  | tar -C ~/.local -xf -
        """,
        cwd=base,
        shell=True,
        check=True,
    )


def install():
    if is_linux() and is_docker_installed():
        install_delta()
        install_fish()
        install_tmux()

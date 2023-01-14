"""Install from source on hosts where all we have for certain is Docker"""

import platform
from pathlib import Path
from subprocess import run
from uuid import uuid4

FISH_VERSION = "3.6.0"
TMUX_VERSION = "3.3a"

#
# General purpose dev-environment things.  Anything project specific shouldn't
# be here as it'll clutter up everything else.
#
PYTHON_PACKAGES = {
    "black",
    "docker-compose",
    "isort",
    "mypy",
    "pre_commit",
    "pycodestyle",
    "pylint",
    "pytest",
    "python-lsp-server",  # Newer than python-language-server
}


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


def install_fish():
    if FISH_VERSION in shell("fish --version"):
        return
    docker_install("fish", FISH_VERSION)


def install_tmux():
    if TMUX_VERSION in shell("tmux -V"):
        return
    docker_install("tmux", TMUX_VERSION)


def install_python_packages():
    run(
        [
            "pip3",
            "install",
            "--quiet",
            "--user",
            *PYTHON_PACKAGES,
        ],
        check=True,
    )


def docker_install(name, version):
    image_name = f"{name}-{uuid4()}"
    base = Path(__file__).parent / name
    container_name = f"{name}-{uuid4()}"
    run(
        f"""
        set -ex
        docker build --tag {image_name} --build-arg VERSION={version} .
        docker run --name {container_name} --rm {image_name} \
            tar -C /out -cf - .  | tar -C ~/.local -xf -
        docker container rm -f {container_name}
        docker image rm {image_name}
        """,
        cwd=base,
        shell=True,
        check=True,
    )


def install():
    if is_linux() and is_docker_installed():
        install_fish()
        install_tmux()
    install_python_packages()

"""Install from source on hosts where all we have for certain is Docker"""

import platform
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
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
    docker_install(
        name="fish",
        dockerfile=rf"""
        FROM debian:latest
        ENV DEBIAN_FRONTEND=noninteractive
        RUN apt update
        RUN apt install --yes --no-install-recommends \
            build-essential ca-certificates cmake git libncurses-dev \
            ninja-build
        WORKDIR /src
        RUN git clone --depth 1 --branch {FISH_VERSION} \
            https://github.com/fish-shell/fish-shell.git .
        RUN cmake \
            -DCMAKE_INSTALL_PREFIX=/out \
            -B build/ \
            .
        RUN make -C build/
        RUN make -C build/ install
        """,
    )


def install_tmux():
    if TMUX_VERSION in shell("tmux -V"):
        return
    docker_install(
        name="tmux",
        dockerfile=rf"""
        FROM debian:latest
        ENV DEBIAN_FRONTEND=noninteractive
        RUN apt update
        RUN apt install --yes --no-install-recommends \
            autoconf automake bison build-essential ca-certificates git \
            libevent-dev libncurses-dev pkg-config
        WORKDIR /src
        RUN git clone --depth 1 --branch {TMUX_VERSION} \
            https://github.com/tmux/tmux.git .
        RUN sh autogen.sh
        RUN ./configure --enable-static --prefix /out
        RUN make install
        """,
    )


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


def docker_install(name, dockerfile):
    image_name = f"{name}-{uuid4()}"
    container_name = f"{name}-{uuid4()}"
    with TemporaryDirectory() as tempdir:
        (Path(tempdir) / "Dockerfile").write_text(dockerfile)
        run(
            f"""
            set -ex
            docker build --tag {image_name} .
            docker run \
                --name {container_name} \
                --rm \
                {image_name} \
                tar -C /out -cf - . > tar
            tar -C ~/.local -xf tar
            docker container rm -f {container_name}
            docker image rm {image_name}
            """,
            cwd=tempdir,
            shell=True,
            check=True,
        )


def install():
    if is_linux() and is_docker_installed():
        install_fish()
        install_tmux()
    install_python_packages()


if __name__ == "__main__":
    install()

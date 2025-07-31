from shutil import which

from microdot.packages.source import get_version, install_from_script, parse_version

VERSION = "25.05.1"

SCRIPT = r"""
set -ex

sudo apt install \
    cargo \
    clang \
    gcc \
    libdbus-1-dev \
    libdisplay-info-dev \
    libegl1-mesa-dev \
    libgbm-dev \
    libinput-dev \
    libpango1.0-dev \
    libpipewire-0.3-dev \
    libseat-dev \
    libsystemd-dev \
    libudev-dev \
    libwayland-dev \
    libxkbcommon-dev \
    ;

git clone \
    --depth 1 \
    --branch "v$1" \
    https://github.com/YaLTeR/niri.git

cd niri

cargo build --release

mkdir -p ../out/bin

mv target/release/niri ../out/bin
"""


def install():
    if which("niri"):
        if get_version("niri", "--version") >= parse_version(VERSION):
            return
    install_from_script(SCRIPT, VERSION)


if __name__ == "__main__":
    install()

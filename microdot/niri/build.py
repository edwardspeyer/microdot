from shutil import which

from microdot import get_version, install_from_script, is_ssh_remote, parse_version

VERSION = "25.11"

SCRIPT = r"""
set -ex

if [ "$NIRI_SOCKET" ]
then
  echo >&2 "Cannot run from an existing niri session!"
  exit 2
fi

sudo apt install \
    cargo \
    clang \
    foot \
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
    sccache \
    ;

git clone \
    --depth 1 \
    --branch "v$1" \
    https://github.com/YaLTeR/niri.git

cd niri

env RUSTC_WRAPPER=sccache cargo build --release

mkdir -p ../out/bin

mv target/release/niri ../out/bin
"""


def build() -> None:
    if is_ssh_remote():
        return
    if which("niri"):
        if get_version("niri", "--version") >= parse_version(VERSION):
            return
    install_from_script(SCRIPT, VERSION)

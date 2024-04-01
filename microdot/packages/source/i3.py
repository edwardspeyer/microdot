import platform
from shutil import which

from microdot.packages.source import get_version, install_from_script, parse_version

VERSION = "4.22"

SCRIPT = r"""
set -ex
sudo apt install --yes --no-install-recommends \
  build-essential libcairo2-dev libev-dev libpango1.0-dev libpcre3-dev \
  libstartup-notification0-dev libstartup-notification0-dev libxcb-cursor-dev \
  libxcb-icccm4-dev libxcb-keysyms1-dev libxcb-randr0-dev libxcb-shape0-dev \
  libxcb-util0-dev libxcb-xinerama0-dev libxcb-xkb-dev libxcb-xkb-dev \
  libxcb-xrm-dev libxkbcommon-dev libxkbcommon-x11-dev libyajl-dev \
  libyajl-dev meson ninja-build suckless-tools
wget "https://i3wm.org/downloads/i3-${1}.tar.xz"
tar xf "i3-${1}.tar.xz"
out="$PWD/out"
cd "i3-${1}"
mkdir -p build
cd build
meson --prefix $out ..
ninja
meson install
"""


def install():
    if which("i3"):
        if get_version("i3", "--version") >= parse_version(VERSION):
            return
    assert platform.system() == "Linux"
    install_from_script(SCRIPT, VERSION)


if __name__ == "__main__":
    install()

import platform
from shutil import which

from microdot.packages.source import get_version, install_from_script, parse_version

VERSION = "3.6.0"

SCRIPT = r"""
set -ex

sudo apt install --yes --no-install-recommends \
  build-essential ca-certificates ccache cmake git libncurses-dev \
  ninja-build

git clone --depth 1 --branch "$1" \
  https://github.com/fish-shell/fish-shell.git .

cmake -DCMAKE_INSTALL_PREFIX=out -B build/ .
make -C build/
make -C build/ install
rm -f out/bin/fish_key_reader out/bin/fish_indent
"""


def install():
    if which("fish"):
        if get_version("fish", "--version") >= parse_version(VERSION):
            return
    assert platform.system() == "Linux"
    install_from_script(SCRIPT, VERSION)


if __name__ == "__main__":
    install()

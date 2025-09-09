import platform
from shutil import which

from microdot import register
from microdot.build import get_version, install_from_script, parse_version

VERSION = "3.3a"

SCRIPT = r"""
set -ex
sudo apt install --yes --no-install-recommends \
  autoconf automake bison build-essential ca-certificates ccache git \
  libevent-dev libncurses-dev pkg-config
git clone --depth 1 --branch "$1" https://github.com/tmux/tmux.git .
sh autogen.sh
./configure --enable-static --prefix ./out
make install
"""


@register
def install():
    if which("tmux"):
        if get_version("tmux", "-V") >= parse_version(VERSION):
            return

    assert platform.system() == "Linux"
    install_from_script(SCRIPT, VERSION)

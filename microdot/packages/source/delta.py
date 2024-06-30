import platform
from shutil import which

from microdot.packages.source import get_version, install_from_script, parse_version

VERSION = "0.15.1"

SCRIPT = r"""
set -ex
wget https://github.com/dandavison/delta/releases/download/${1}/git-delta_${1}_amd64.deb
dpkg -x git-delta*.deb v
mkdir -p out/bin
cp v/usr/bin/delta out/bin/
"""


def install():
    if which("delta"):
        if get_version("delta", "-V") >= parse_version(VERSION):
            return
    assert platform.system() == "Linux", "Can only install delta in linux"
    install_from_script(SCRIPT, VERSION)

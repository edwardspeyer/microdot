import platform
from shutil import which

from microdot import install_from_script

VERSION = "0.8.1"

SCRIPT = r"""
set -ex

sudo apt install --yes --no-install-recommends \
    cargo libxcb-cursor-dev

git clone --depth 1 --branch v"$1" \
  https://github.com/Supreeeme/xwayland-satellite.git

cd xwayland-satellite
env RUSTC_WRAPPER=sccache cargo build --release

mkdir -p ../out/bin/
cp target/release/xwayland-satellite ../out/bin/
"""


def build():
    if which("xwayland-satellite"):
        return
    assert platform.system() == "Linux"
    install_from_script(SCRIPT, VERSION)

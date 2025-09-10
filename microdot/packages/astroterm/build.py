from shutil import which

from microdot import get_debian_version, install_from_script


def install() -> None:
    if which("astroterm"):
        return

    if (v := get_debian_version()) and isinstance(v, float) and v < 13:
        print("This Debian is too old for building astroterm")
        return

    breakpoint()

    install_from_script(
        r"""
        set -ex
        mkdir -p out/bin
        sudo apt install \
            meson build-essential libargtable2-dev libncurses-dev xxd
        git clone --depth 1 --branch 'v1.0.8' \
            https://github.com/da-luce/astroterm.git src
        cd src
        curl -L -o data/bsc5 \
            https://web.archive.org/web/20231007085824if_/http://tdc-www.harvard.edu/catalogs/BSC5
        meson setup build
        meson compile -C build
        mv build/astroterm ../out/bin
        """
    )


if __name__ == "__main__":
    install()

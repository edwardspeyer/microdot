import platform
import re
from pathlib import Path
from shutil import copy
from subprocess import check_output, run
from tempfile import TemporaryDirectory

from microdot import is_ssh_remote


def install_macosx():
    # 10.15 – Catalina – October 2019
    terminal_app = Path("/System/Applications/Utilities/Terminal.app")
    paths = list(terminal_app.glob("**/SF*Mono*.otf"))
    assert paths, "fonts not found"
    user_fonts = Path.home() / "Library/Fonts"
    for source in paths:
        target = user_fonts / source.name
        if target.exists():
            continue
        print("  FONT", source.name)
        copy(source, target)


def fc_has_font(name: str) -> bool:
    log = check_output("fc-list", text=True)
    return re.search(name, log) is not None


def install_linux_iosevka():
    if fc_has_font("Iosevka Term"):
        print("  OK  ", "Iosevka installed")
        return

    with TemporaryDirectory() as tmp:
        run(
            r"""
            set -ex
            wget -O font.zip \
                https://github.com/be5invis/Iosevka/releases/download/v33.2.7/SuperTTC-SGr-IosevkaTerm-33.2.7.zip
            unzip font.zip
            mv SGr-IosevkaTerm.ttc ~/.local/share/fonts
            """,
            shell=True,
            cwd=tmp,
            check=True,
        )


def install_linux_sf_mono():
    if fc_has_font("SF Mono"):
        print("  OK  ", "SF Mono installed")
        return

    with TemporaryDirectory() as tmp:
        run(
            """
            set -ex
            url="https://devimages-cdn.apple.com/design/resources/download/SF-Mono.dmg"
            sudo apt install --yes 7zip cpio
            wget -O dmg $url
            ls -l dmg
            file dmg
            7zz x dmg
            7zz x "SFMonoFonts/SF Mono Fonts.pkg"
            cpio -idv -F "Payload~"
            find .
            """,
            shell=True,
            cwd=tmp,
            check=True,
        )
        target = Path.home() / ".local" / "share" / "fonts"
        target.mkdir(exist_ok=True, parents=True)
        for source in Path(tmp).glob("**/*.otf"):
            print("  FONT", source.name)
            copy(source, target)


def install_linux():
    install_linux_iosevka()
    install_linux_sf_mono()


def install():
    if is_ssh_remote():
        return
    if platform.system() == "Darwin":
        install_macosx()
    elif platform.system() == "Linux":
        install_linux()

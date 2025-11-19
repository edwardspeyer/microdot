import platform
import re
from pathlib import Path
from shutil import copy, which
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


def has_fc() -> bool:
    return which("fc-list") is not None


def fc_has_font(name: str) -> bool:
    log = check_output("fc-list", text=True)
    return re.search(name, log) is not None


def install_linux_iosevka() -> None:
    if not has_fc():
        return

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
            mkdir -p ~/.local/share/fonts/
            mv SGr-IosevkaTerm.ttc ~/.local/share/fonts
            """,
            shell=True,
            cwd=tmp,
            check=True,
        )


def install_linux() -> None:
    install_linux_iosevka()


def install():
    if is_ssh_remote():
        return
    if platform.system() == "Darwin":
        install_macosx()
    elif platform.system() == "Linux":
        install_linux()

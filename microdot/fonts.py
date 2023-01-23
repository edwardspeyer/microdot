import platform
from pathlib import Path
from shutil import copy


def install():
    if platform.system() == "Darwin":
        install_macosx()


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

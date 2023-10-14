import platform
from pathlib import Path
from shutil import copy


def install(*sources: Path):
    for source in sources:
        _install_one(source)


def _install_one(source: Path):
    first_letter = source.name[0]

    if platform.system() == "Linux":
        sub = first_letter
    elif platform.system() == "Darwin":
        sub = f"{ord(first_letter):x}"
    else:
        raise Exception("unknown platform")

    destination = Path.home() / ".terminfo" / sub / source.name
    if destination.exists():
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    print("  TERMINFO", source)
    copy(source, destination)
